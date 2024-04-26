import streamlit as st
import snowflake.connector
import bcrypt
import streamlit as st
import snowflake.connector
from snowflake.connector import DictCursor
import openai
import os
from PIL import Image, UnidentifiedImageError
import re
import html
import requests
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv
from CSS_UI import apply_custom_styles


# Snowflake connection parameters
conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database='USER_DATABASE',
    schema='USER'
)

import streamlit as st

# Set up session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Define your pages as functions
def Login():
    # with st.expander("Login"):
    # # st.title("Login to NewsScope")
    #     username = st.text_input("Username")
    #     password = st.text_input("Password", type="password")
    #     login_button = st.button("Login", key="login_button")
        
    #     if login_button:
    #         cursor = conn.cursor()
    #         cursor.execute(f"SELECT * FROM USERS_CRED WHERE username = '{username}'")
    #         user = cursor.fetchone()
    #         if user is not None and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
    #             st.session_state['logged_in'] = True
    #             st.success("Logged in successfully.")
    #             render_sidebar()
    #         else:
    #             st.error("Incorrect username or password.")
    st.markdown("""
        <style>
        .login-title {
            font-size: 24px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    with st.expander("LOGIN", expanded=True):
        st.markdown('<p class="login-title">Login</p>', unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login", key="login_button")
        
        if login_button:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM USERS_CRED WHERE username = '{username}'")
            user = cursor.fetchone()
            if user is not None and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username 
                st.success("Logged in successfully.")
                render_sidebar()
            else:
                st.error("Incorrect username or password.")

def logout():
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.sidebar.success("You have been logged out.")
        st.experimental_rerun()



def signup():
    st.markdown("""
        <style>
        .signup-title {
            font-size: 24px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Welcome to NewsScope</h1>", unsafe_allow_html=True)
    with st.expander("SIGN UP", expanded=True):
        st.markdown('<p class="signup-title">Sign up</p>', unsafe_allow_html=True)
        new_username = st.text_input("Choose Username", key="signup_username")
        new_password = st.text_input("Choose Password", type="password", key="signup_password")
        signup_button = st.button("Sign Up")

        if signup_button:
            if new_username and new_password:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM USERS_CRED WHERE username = %s", (new_username,))
                user_exists = cursor.fetchone()
                if user_exists:
                    st.error("Username already exists. Choose a different username.")
                else:
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("INSERT INTO USERS_CRED (username, password) VALUES (%s, %s)", 
                                   (new_username, hashed_password.decode('utf-8')))
                    conn.commit()
                    st.success("Signup successful. Please login with your new credentials.")
                cursor.close()
            else:
                st.warning("Please enter both a username and a password.")

def Welcome_To_NewsScope():
    st.markdown("<h1 style='text-align: center;'>Welcome to NewsScope</h1>", unsafe_allow_html=True)

def Customised_Keyword_Recommendation():

    # Path to the file where keywords will be stored
    keywords_file = "saved_keywords.txt"

    def save_keywords(keywords):
        """Save the keywords to a file, excluding any empty strings."""
        keywords = [kw for kw in keywords if kw]  # Filter out any empty strings
        with open(keywords_file, "w") as f:
            f.write("\n".join(keywords))

    def load_keywords():
        """Load the keywords from a file, excluding any empty strings."""
        try:
            with open(keywords_file, "r") as f:
                return [kw for kw in f.read().split("\n") if kw]  # Filter out any empty strings
        except FileNotFoundError:
            return []  # Return an empty list if the file does not exist

    def remove_keyword(keyword):
        """Remove a keyword and save the updated list."""
        saved_keywords.remove(keyword)
        save_keywords(saved_keywords)
        st.experimental_rerun()

    # Assuming you have the connection details in 'conn_params'
    conn_params = {
        "user": st.secrets["snowflake"]["user"],
        "password": st.secrets["snowflake"]["password"],
        "account": st.secrets["snowflake"]["account"],
        "warehouse": st.secrets["snowflake"]["warehouse"],
        "database": st.secrets["snowflake"]["database"],
        "schema": st.secrets["snowflake"]["schema"],
    }

    def fetch_headlines(top_five=False):
        """Fetch headlines, content, and image URLs from Snowflake database."""
        with snowflake.connector.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                if top_five:
                    cur.execute("SELECT HEADINGS, CONTENT, IMAGE FROM COMBINEDNEWSFEED ORDER BY ENTRY_DATE DESC LIMIT 5")
                else:
                    cur.execute("SELECT HEADINGS, CONTENT, IMAGE FROM COMBINEDNEWSFEED")
                return cur.fetchall()  # Returns a list of tuples (headline, content, image_url)

    def normalize_whitespace(text):
        """Normalize whitespace in the content."""
        return re.sub(r'\s+', ' ', text).strip()

    # Initialize a session state to track if a keyword has been searched
    if 'search_initiated' not in st.session_state:
        st.session_state.search_initiated = False

    # Load saved keywords
    saved_keywords = load_keywords()

    # Streamlit app setup
    st.markdown("""
        <h1 style='text-align: center;'>My News Feed</h1>
        """, unsafe_allow_html=True)

    # Input text box for adding keywords
    user_input = st.text_input("Enter keywords to search for relevant news headlines:")

    # "Add" button for adding keywords
    add_button = st.button("Add")
    if add_button and user_input:
        st.session_state.search_initiated = True  # Set the search state to True
        user_input_keywords = [kw.strip().lower() for kw in user_input.split(",") if kw.strip()]
        existing_keywords = set(user_input_keywords) & set(saved_keywords)
        if existing_keywords:
            st.warning(f"Keyword already exists: {', '.join(existing_keywords)}")
        else:
            new_keywords = set(user_input_keywords) | set(saved_keywords)
            save_keywords(list(new_keywords))
            saved_keywords = list(new_keywords)  # Update the list of saved keywords
            st.experimental_rerun()

    # Displaying Keyword Buttons
    if saved_keywords:
        st.write("Click a keyword to filter headlines or click 'x' to remove it:")
        for keyword in saved_keywords:
            col1, col2 = st.columns([0.9, 0.1], gap="small")
            with col1:
                if keyword and st.button(keyword, key=f"btn_{keyword}"):
                    matching_headlines = [(headline, normalize_whitespace(content), image) for headline, content, image in fetch_headlines() if re.search(rf"\b{keyword}\b", headline.lower())]
                    if matching_headlines:
                        st.subheader(f"Headlines for '{keyword}':")
                        for headline, content, image in matching_headlines:
                            with st.expander(headline):
                                if image:
                                    try:
                                        st.image(image, caption=headline)
                                    except Exception as e:
                                        st.write(f"Failed to load image.")
                                st.write(content)
                    else:
                        st.write(f"No headlines found for '{keyword}'.")
            with col2:
                if keyword and st.button("x", key=f"remove_{keyword}"):
                    remove_keyword(keyword)

    # "Recommend me" button for headline recommendations
    recommend_button = st.button("Recommend Headlines")
    if recommend_button:
        if saved_keywords:
            st.subheader("Recommended Headlines")
            headlines_with_content = fetch_headlines()
            headline_scores = [(headline, content, image, sum(re.search(rf"\b{keyword}\b", headline.lower()) is not None for keyword in saved_keywords)) for headline, content, image in headlines_with_content]
            recommended_headlines = sorted([(headline, content, image) for headline, content, image, score in headline_scores if score > 0], key=lambda x: headline_scores[headlines_with_content.index((x[0], x[1], x[2]))][3], reverse=True)     
            for headline, content, image in recommended_headlines[:5]:
                with st.expander(headline):
                    if image:
                        try:
                            st.image(image, caption=headline)
                        except Exception as e:
                            st.write(f"Failed to load image")
                    st.write(content)
        else:
            st.write("Please add some keywords for recommendations.")

    # Fetch top 5 news items if no search has been initiated
    if not st.session_state.search_initiated:
        top_five_news = fetch_headlines(top_five=True)
        # Streamlit app setup
        st.markdown("""
            <h1 style='text-align: center;'>Top 5 News</h1>
            """, unsafe_allow_html=True)    
        for headline, content, image in top_five_news:
            with st.expander(headline):
                if image:
                    try:
                        st.image(image, caption=headline)
                    except Exception as e:
                        st.write(f"Failed to load image.")
                st.write(normalize_whitespace(content))

def Industry_Specific_Filters():

    st.markdown("""
        <h1 style='text-align: center;'>Industry News Feed</h1>
        """, unsafe_allow_html=True)

    st.markdown("""
    This page allows users to filter news feeds by specific industries. Users can select their industry of interest to view relevant news.
    """)

    import snowflake.connector

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

    # Query to retrieve unique industries
    industry_query = "SELECT DISTINCT INDUSTRY FROM COMBINEDNEWSFEED"

    # Execute the query
    cur = conn.cursor()
    cur.execute(industry_query)
    industries = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Extract the list of industries for the dropdown
    industry_list = [row[0] for row in industries]  # Assumes that the Industry column is the first column

    # Dropdown for selecting an industry
    selected_industry = st.selectbox("Select an Industry", industry_list)

    # Connect to Snowflake again to get filtered headlines
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

    # Query to retrieve headlines based on the selected industry
    headline_query = """
    SELECT HEADINGS
    FROM COMBINEDNEWSFEED
    WHERE INDUSTRY = %s
    """

    # Execute the query with the selected industry
    cur = conn.cursor()
    cur.execute(headline_query, (selected_industry,))
    headlines = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Display headlines
    for headline in headlines:
        st.write(headline[0])


def Summary_Generation():
    # Use markdown to create a styled header
    st.markdown("<h1 style='text-align: center; color: #333;'>NewScope: Pocket Summary</h1>", unsafe_allow_html=True)

    from finalproject_summarytrial import generate_summary_for_headline  # Importing your summary function

    # Snowflake connection parameters
    conn_params = {
        "user": st.secrets["snowflake"]["user"],
        "password": st.secrets["snowflake"]["password"],
        "account": st.secrets["snowflake"]["account"],
        "warehouse": st.secrets["snowflake"]["warehouse"],
        "database": st.secrets["snowflake"]["database"],
        "schema": st.secrets["snowflake"]["schema"],
    }

    # Establish connection to Snowflake
    ctx = snowflake.connector.connect(**conn_params)
    cs = ctx.cursor()

    # Query to retrieve data
    query = "SELECT * FROM COMBINEDNEWSFEED"  
    cs.execute(query)

    # Fetch the result set from the cursor and deliver it as a Pandas DataFrame
    df = cs.fetch_pandas_all()

    # Close the cursor and the connection
    cs.close()
    ctx.close()

    # Use markdown to create a styled header
    #st.markdown("<h1 style='text-align: center; color: #333;'>AI News Summary</h1>", unsafe_allow_html=True)
    # Call the function to apply custom styles
    apply_custom_styles()


    # Use the dataframe from Snowflake
    industries = ['All'] + df['INDUSTRY'].unique().tolist()

    # Selecting an industry
    industry_filter = st.selectbox('Select an industry to filter news', options=industries)

    # Selecting a headline
    headlines = df['HEADINGS'].tolist() if industry_filter == 'All' else df[df['INDUSTRY'] == industry_filter]['HEADINGS'].tolist()
    selected_headline = st.selectbox('Select a headline to summarize', options=headlines)

    # Button to generate summary for selected headline
    if st.button('Generate Summary for Selected Headline'):
        if selected_headline:
            while True:
                with st.spinner('Generating summary...'):
                    augmented_queries = generate_summary_for_headline(selected_headline)
                    if augmented_queries:
                        st.subheader('Summary:')
                        for summary in augmented_queries:
                            st.markdown(f'<div class="summary-text">{augmented_queries}</div>', unsafe_allow_html=True)
                        break
        else:
            st.error('Please select a headline to generate a summary.')


    # Clear summary button
    if st.button('Clear Summary'):
        st.write(" ")

def Natural_Language_Query_Search():
    load_dotenv()

    api_key = os.getenv('api_key')
    client = openai.OpenAI(api_key=api_key)

    def create_snowflake_connection():
        return snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )

    def fetch_news_data():
        conn = create_snowflake_connection()
        try:
            with conn.cursor(snowflake.connector.DictCursor) as cur:
                cur.execute("SELECT headings, content, image FROM combinednewsfeed")
                return cur.fetchall()
        except Exception as e:
            st.error("Failed to fetch data from Snowflake: " + str(e))
        finally:
            conn.close()

    def normalize_whitespace(text):
        text = html.unescape(text)  # Unescape any HTML entities
        text = text.replace(u'\xa0', u' ')  # Replace non-breaking spaces with regular spaces
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        return text.strip()

    def rank_headlines(query, headlines):
        primer = """
        As a news headline assistant, your role is to respond to user queries by identifying and presenting the most relevant news headlines. Here are the guidelines:
        1. Understand the user's query to determine the key subjects or keywords.
        2. Search for headlines that completely match the query focusing on specific people, places, or issues mentioned in the query.
        3. Ensure the headlines are relevant and up-to-date, directly relating to the query without including unrelated information.
        4. Display the headlines in a ranked list based on their relevance to the query, with the most relevant headline appearing first. Provide no more than 5 headlines.
        5. If no relevant headlines are found, communicate clearly to the user with the response: 'No other relevant news headlines found for your query.'
        6. Avoid duplicates and ensure each headline presented offers unique information.
        """
        prompt = f"""
        Here's a query from a user: '{query}'. Considering the query, identify and present only the most relevant and specific headlines with those specific keywords. 
        Exclude any headlines that do not directly address the query's subject. Here are the headlines to evaluate:
        """
        for headline in headlines:
            prompt += f"- {headline}\n"

        messages = [{"role": "system", "content": primer}, {"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",        
        )

        ranked_headlines_str = response.choices[0].message.content.strip()
        ranked_headlines_list = [
            line.split('. ', 1)[1].strip(' *') if '. ' in line else line.strip(' *')
            for line in ranked_headlines_str.splitlines()
        ]

        return ranked_headlines_list

    def main():
        apply_custom_styles() 
        st.markdown("<h1 style='text-align: center;'>NewsNet</h1>", unsafe_allow_html=True)
        query = st.text_input("Enter your news search query:")

        if 'news_data' not in st.session_state or st.button("Search"):
            st.session_state.news_data = fetch_news_data()
            headlines = {
                news['HEADINGS']: {
                    'content': normalize_whitespace(news['CONTENT']),
                    'image': None if news['IMAGE'] == "image not found!" else news['IMAGE']
                }
                for news in st.session_state.news_data
            }
            st.session_state.headlines = headlines
            if query:
                st.session_state.ranked_headlines = rank_headlines(query, list(headlines.keys()))

        if 'ranked_headlines' in st.session_state:
            selected_headline = st.selectbox('Select a headline:', st.session_state.ranked_headlines)
            st.write("You selected:", selected_headline)
            selected_news = st.session_state.headlines.get(selected_headline)

            if selected_news:
                st.subheader('Content:')
                with st.container():
                    st.markdown(f'<div id="customContent">{selected_news["content"]}</div>', unsafe_allow_html=True)
                
                if selected_news['image']:
                    try:
                        response = requests.get(selected_news['image'])
                        response.raise_for_status()
                        img = Image.open(BytesIO(response.content))
                        st.image(img, use_column_width=True)
                    except (requests.exceptions.HTTPError, requests.exceptions.RequestException, UnidentifiedImageError):
                        st.write("Image not available.")
                else:
                    st.write("No image available.")
            else:
                st.write("Details for the selected headline are not available.")

    if __name__ == "__main__":
        main()

# Define a function to render the sidebar and control page flow
def render_sidebar():
    st.sidebar.title("Navigation")
    # You can put your login/logout buttons in the sidebar
    if st.session_state['logged_in']:
        page = st.sidebar.radio('Go to', ('Welcome to NewsScope','My News Feed', 'Industry News Feed', 'NewsScope: Pocket Summary', 'NewsNet'))
        if page == 'Welcome to NewsScope':
            Welcome_To_NewsScope()
        elif page == 'My News Feed':
            Customised_Keyword_Recommendation()
        elif page == 'Industry News Feed':
            Industry_Specific_Filters()
        elif page == 'NewsScope: Pocket Summary':
            Summary_Generation()
        elif page == 'NewsNet':
            Natural_Language_Query_Search()
    else:
        st.sidebar.text("Please log in to navigate.")

# Your main app logic
def main():
    # st.title("Welcome to NewsScope")
        apply_custom_styles()
        if not st.session_state['logged_in']:
                signup()
                Login()
                
        else:
                render_sidebar()
                logout()


# Run the main function
if __name__ == "__main__":
    main()