import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import snowflake.connector
load_dotenv()
def scrape_technology():
    def create_snowflake_connection():
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema='WIRED'
        )
        return conn

    def insert_into_snowflake(articles, conn):
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO WIRED_NEWSFEED (headings, links, content, industry, entry_date, image)
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
        link_classes = ['SummaryItemHedLink-civMjp ejgyuy summary-item-tracking__hed-link summary-item__hed-link',
                        'SummaryItemHedLink-civMjp kFnjUG summary-item-tracking__hed-link summary-item__hed-link']
        headline_url_pairs = []

        for link_class in link_classes:
            links = soup.find_all('a', class_=link_class)
            for link in links:
                headline = link.find(['h2', 'h3'], class_='SummaryItemHedBase-hiFYpQ')
                if headline:
                    headline_text = headline.text.strip()
                    url = urljoin(base_url, link['href'])
                    headline_url_pairs.append((headline_text, url))

        return headline_url_pairs

    def scrape_article_content(url):
        page_content = get_page_content(url)
        if not page_content:
            return None, "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

        soup = BeautifulSoup(page_content, 'html.parser')
        article_content_div = soup.find('div', class_='body__inner-container')
        image_container = soup.find('div', class_='aspect-ratio--overlay-container')
        image_url = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"  # Default image

        if image_container:
            img_tag = image_container.find('img')
            if img_tag and 'src' in img_tag.attrs:
                image_url = img_tag['src']

        article_text = None
        if article_content_div:
            paragraphs = article_content_div.find_all('p')
            article_text = ' '.join(paragraph.get_text() for paragraph in paragraphs)
            return article_text, image_url
        else:
            print(f"Article content not found for URL: {url}")
            return None, image_url

    def main():
        base_url = 'https://www.wired.com'
        today_date = datetime.now().strftime("%Y-%m-%d")
        conn = create_snowflake_connection()
        headlines_and_urls = scrape_headlines_and_urls(base_url)
        complete_articles = []

        for headline, url in headlines_and_urls:
            content, image = scrape_article_content(url)
            if headline and url and content:  # Check if any field is blank and skip writing that row if true
                complete_articles.append((headline, url, content, 'Technology', today_date, image))

        if complete_articles:
            insert_into_snowflake(complete_articles, conn)

        conn.close()

    if __name__ == '__main__':
        main()
