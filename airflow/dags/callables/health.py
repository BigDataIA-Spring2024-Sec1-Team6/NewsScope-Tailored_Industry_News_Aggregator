import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
import snowflake.connector
from urllib.parse import urljoin  # Proper function for joining URLs
load_dotenv()
def scrape_health():
    def create_snowflake_connection():
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema='CNN'
        )
        return conn

    def insert_into_snowflake(data, conn):
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO cnn_newsfeed (headings, links, content, industry, entry_date, image)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(sql, data)
            conn.commit()
        finally:
            cursor.close()

    def get_page_content(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve the page: {url}")
            return None

    def scrape_headlines_and_urls(base_url):
        page_content = get_page_content(base_url)
        if not page_content:
            return []

        soup = BeautifulSoup(page_content, 'html.parser')
        links = soup.find_all('a', class_='container__link--type-article')
        headline_url_pairs = []

        for link in links:
            headline = link.find('span', class_='container__headline-text')
            if headline:
                headline_text = headline.text.strip()
                url = urljoin(base_url, link['href'])
                headline_url_pairs.append((headline_text, url))

        return headline_url_pairs

    def scrape_article_content_and_image(url):
        page_content = get_page_content(url)
        if not page_content:
            return None, "No Image Found"

        soup = BeautifulSoup(page_content, 'html.parser')
        article_content_div = soup.find('div', class_='article__content-container')
        image_container = soup.find('div', class_='image__container')

        article_text = None
        image_url = "No Image Found"

        if article_content_div:
            paragraphs = article_content_div.find_all('p')
            article_text = ' '.join(paragraph.get_text() for paragraph in paragraphs)

        if image_container:
            img_tag = image_container.find('img')
            if img_tag and 'src' in img_tag.attrs:
                image_url = img_tag['src']

        return article_text, image_url

    # The base URL from which you're starting the scrape
    base_url = 'https://www.cnn.com/health'

    # Scrape headlines and their corresponding URLs
    headlines_and_urls = scrape_headlines_and_urls(base_url)

    # Get the current date in YYYY-MM-DD format
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Establish a connection to Snowflake
    conn = create_snowflake_connection()

    # Prepare the data to be inserted
    data_to_insert = []
    for headline, url in headlines_and_urls:
        content, image = scrape_article_content_and_image(url)
        if headline and url and content:
            data_to_insert.append((headline, url, content, 'Health', today_date, image))

    # Insert data into Snowflake
    if data_to_insert:
        insert_into_snowflake(data_to_insert, conn)

    # Close the Snowflake connection
    conn.close()

    print("Data has been successfully written to your Snowflake database.")