import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import snowflake.connector
load_dotenv()
def scrape_fashion():
    
    def create_snowflake_connection():
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema='CNBC'
        )
        return conn

    def insert_into_snowflake(articles, conn):
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO CNBC_NEWSFEED (headings, links, content, industry, entry_date, image)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(sql, articles)
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
        containers = soup.find_all('div', class_='Card-titleContainer')
        headline_url_pairs = []

        for container in containers:
            link = container.find('a', class_='Card-title')
            if link and link.text:
                headline_text = link.text.strip()
                url = urljoin(base_url, link['href'])
                headline_url_pairs.append((headline_text, url))

        return headline_url_pairs

    def scrape_article_content_and_image(url):
        page_content = get_page_content(url)
        if not page_content:
            return None, "No Image Found"

        soup = BeautifulSoup(page_content, 'html.parser')
        article_content_div = soup.find('div', class_='group')
        image_container = soup.find('div', class_='Card-squareMediaContainer') or soup.find('div', class_='Card-rectangleMediaContainer')

        article_text = None
        image_url = "No Image Found"  # Default text when no image found

        if article_content_div:
            paragraphs = article_content_div.find_all('p')
            article_text = ' '.join(paragraph.get_text() for paragraph in paragraphs)

        if image_container:
            img_tag = image_container.find('img')
            if img_tag and 'src' in img_tag.attrs:
                image_url = img_tag['src']
            else:
                secondary_image_container = soup.find('div', class_='InlineImage-imageContainer')
                if secondary_image_container:
                    secondary_img_tag = secondary_image_container.find('img')
                    if secondary_img_tag and 'src' in secondary_img_tag.attrs:
                        image_url = secondary_img_tag['src']

        return article_text, image_url

    def main():
        base_url = 'https://www.cnbc.com/fashion'
        today_date = datetime.now().strftime("%Y-%m-%d")
        conn = create_snowflake_connection()
        headlines_and_urls = scrape_headlines_and_urls(base_url)
        complete_articles = []

        for headline, url in headlines_and_urls:
            content, image = scrape_article_content_and_image(url)
            if headline and url and content:  # Ensure all fields are non-empty
                complete_articles.append((headline, url, content, 'Fashion', today_date, image))

        if complete_articles:
            insert_into_snowflake(complete_articles, conn)

        conn.close()

    if __name__ == '__main__':
        main()
