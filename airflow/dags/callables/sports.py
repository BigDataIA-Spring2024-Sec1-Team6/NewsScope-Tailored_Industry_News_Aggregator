import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
import snowflake.connector
from urllib.parse import urljoin  # Import for proper URL joining
load_dotenv()
def scrape_sports():
    def create_snowflake_connection():
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema='SI'
        )
        return conn

    def insert_into_snowflake(articles, conn):
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO si_newsfeed (headings, links, content, industry, entry_date, image)
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

    def scrape_main_page(url):
        page_content = get_page_content(url)
        if not page_content:
            return []

        soup = BeautifulSoup(page_content, 'html.parser')
        articles = []
        base_url = 'https://www.si.com'

        for card in soup.find_all('h2', class_='m-ellipsis--text m-card--header-text'):
            link_element = card.find_parent('a')
            if link_element and 'href' in link_element.attrs:
                link = link_element['href']
                if not link.startswith('http'):
                    link = urljoin(base_url, link)
                headline = card.get_text(strip=True).strip()
                if headline:
                    articles.append((headline, link))
                else:
                    print("No headline found for an article.")
            else:
                print("No link found for an article headline.")

        return articles

    def scrape_article_details(url):
        page_content = get_page_content(url)
        if not page_content:
            return ("Content could not be retrieved", "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg")

        soup = BeautifulSoup(page_content, 'html.parser')
        content_blocks = soup.find_all('div', class_='m-detail--body')
        image_url = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"  # Default image

        # Scrape for the image
        img_tag = soup.find('img')
        if img_tag and 'src' in img_tag.attrs:
            image_url = img_tag['src']

        if content_blocks:
            details = [block.get_text(strip=True) for block in content_blocks]
            detailed_content = ' '.join(details).strip()
            return (detailed_content if detailed_content else "No detailed content found", image_url)
        else:
            return ("No content found for this article", image_url)

    def main():
        main_url = 'https://www.si.com'
        today_date = datetime.now().strftime("%Y-%m-%d")
        conn = create_snowflake_connection()
        articles_info = scrape_main_page(main_url)
        complete_articles = []

        for headline, link in articles_info:
            content, image = scrape_article_details(link)
            complete_articles.append((headline, link, content, 'Sports', today_date, image))

        if complete_articles:
            insert_into_snowflake(complete_articles, conn)

        conn.close()

    if __name__ == '__main__':
        main()
