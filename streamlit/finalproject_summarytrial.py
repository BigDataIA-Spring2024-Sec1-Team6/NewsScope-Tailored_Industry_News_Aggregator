import pandas as pd
import openai
from pinecone import PodSpec
from pinecone import Index
from pinecone import Pinecone
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
from tqdm.auto import tqdm
import datetime
from time import sleep
import snowflake.connector
import toml
import os
from dotenv import load_dotenv

load_dotenv()

# Load secrets from TOML file
config = toml.load(".streamlit/secrets.toml")

# Snowflake credentials
snowflake_user = config["snowflake"]["user"]
snowflake_password = config["snowflake"]["password"]
snowflake_account = config["snowflake"]["account"]
snowflake_warehouse = config["snowflake"]["warehouse"]
snowflake_database = config["snowflake"]["database"]
snowflake_schema = config["snowflake"]["schema"]

# Initialize your API keys (consider using environment variables or a secure method to store these)
api_key = os.environ.get('api_key')
papi_key = os.environ.get('papi_key')

# Configure the Snowflake connection
conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    warehouse=snowflake_warehouse,
    database=snowflake_database,
    schema=snowflake_schema
)

# Execute a query to load data
df = pd.read_sql("SELECT * FROM COMBINEDNEWSFEED", conn)
conn.close()

# Primer for the bot
primer = "You are a summary generation bot. designed to provide intelligent answers based on the information provided. If the information is not available, you truthfully say, 'I don't know'."

# Pinecone initialization
pinecone = Pinecone(api_key=papi_key)
index_name = 'generate-summary'

# Check if the index exists
# Check if the index exists
all_indexes = pinecone.list_indexes()
if index_name in [idx['name'] for idx in all_indexes]:
    print(f"Index '{index_name}' already exists.")
    index = pinecone.Index(name=index_name)
else:
    print(f"Creating new index '{index_name}'.")
    # Only create the index if it definitely does not exist
    pinecone.create_index(name=index_name, dimension=1536, spec=PodSpec(environment="gcp-starter"))
    index = pinecone.Index(name=index_name)



# OpenAI initialization
client = openai.OpenAI(api_key=api_key)

# Tokenizer and text splitter setup
tokenizer = tiktoken.get_encoding('p50k_base')

def tiktoken_len(text):
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,
    length_function=tiktoken_len,
    separators=["\n\n", "\n", " ", ""]
)

# Function to create embeddings with retry logic
def create_embeddings_with_retry(text, model, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            return client.embeddings.create(input=[text], model=model)
        except Exception as e:
            print(f"Attempt {retries + 1}: Encountered an error - {e}")
            sleep(5)  # wait before retrying
            retries += 1
    raise Exception(f"Failed to create embeddings after {max_retries} retries.")

# Function to generate namespace from headline
def generate_namespace_from_headline(headline):
    title_cleaned = ''.join(char for char in headline if char.isascii())
    namespace = f"{title_cleaned}_Summary"
    namespace = ''.join(char for char in namespace if char.isalnum())
    return namespace

# Function to initialize and upsert data into Pinecone
def initialize_and_upsert_to_pinecone(headline, text, embed_model):
    namespace = generate_namespace_from_headline(headline)
    embed_model ="text-embedding-3-small"
    res = create_embeddings_with_retry(text, embed_model)
    embed = res.data[0].embedding
    id = str(uuid4())
    to_upsert = [(id, embed, {'text': text, 'chunk': 0, 'url': 'default_url'})]
    index.upsert(vectors=to_upsert, namespace=namespace)

# Function to generate summary for a selected headline
def generate_summary_for_headline(selected_headline, embed_model="text-embedding-3-small"):
    # Find the row in the dataframe for the selected headline
    row = df[df['HEADINGS'] == selected_headline].iloc[0]

    # Initialize and upsert data into Pinecone
    initialize_and_upsert_to_pinecone(selected_headline, row['CONTENT'], embed_model)

    # Generate the query embedding
    query = " give me a brief, one paragraph, summary of the article "
    res = client.embeddings.create(
        model=embed_model,
        input=query
    )
    embedding_vector = res.data[0].embedding

    # Perform the query in Pinecone and generate the summary
    namespace = generate_namespace_from_headline(selected_headline)
    query_result = index.query(vector=embedding_vector, top_k=3, namespace=namespace, include_metadata=True)
    contexts = [item['metadata']['text'] for item in query_result['matches']]

    augmented_queries = []
    for context in contexts:
            messages = [{"role": "system", "content": primer}, {"role": "user", "content": context}]
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  
                messages=messages,
                #top_k
                temperature= 0.7
            )

            # If a satisfactory response is obtained, use it
            if "too extensive" not in response.choices[0].message.content.lower():
                augmented_queries.append(response.choices[0].message.content)
                break
    # if not augmented_queries:
    #     augmented_queries = generate_summary_for_headline(selected_headline, text, embed_model)
    return augmented_queries

