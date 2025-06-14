from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from .db import insert_article
import os
import time
import openai

def analyze_with_gpt(content):
    """
    Uses OpenAI's GPT model to analyze news content and suggest a Rotary opportunity.
    Returns the suggestion as a string, or an error message if the API call fails.
    """
    prompt = f"Analyze this news content and suggest a Rotary opportunity:\n\n{content}"
    try:
        # Create OpenAI client using API key from environment variable
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "GPT analysis failed."

def scrape_sources():
    """
    Scrapes a list of Daily Herald archive URLs using Selenium and BeautifulSoup.
    For each page:
      - Extracts the page title and text content.
      - Analyzes the content with GPT for Rotary opportunities.
      - Saves the result to the database.
    """
    urls = [
        "https://www.dailyherald.com/archive/20250614/",
        "https://www.dailyherald.com/archive/20250613/",
        "https://www.dailyherald.com/archive/20250612/",
        "https://www.dailyherald.com/archive/20250611/",
        "https://www.dailyherald.com/archive/20250610/",
    ]

    # Set up Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    for url in urls:
        print(f"Scraping {url} with Selenium...")
        try:
            # Load the page
            driver.get(url)
            time.sleep(3)  # Wait for page to load

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            content = soup.get_text(separator='\n', strip=True)  # Extract all text
            raw_content = driver.page_source  # Save raw HTML
            title = soup.title.string if soup.title else "No Title"
            print(f"Title: {title}\nContent: {content[:1000]}...\n")  # Print preview

            # Analyze content with GPT
            gpt_suggestion = analyze_with_gpt(content)

            # Prepare data for database insertion
            dummy_data = {
                'title': title,
                'url': url,
                'source': 'Daily Herald',
                'content': content,
                'raw_content': raw_content,
                'gpt_suggestion': gpt_suggestion
            }
            try:
                # Insert the article into the database
                insert_article(**dummy_data)
            except Exception as db_err:
                print(f"Database insert failed for {url}: {db_err}")

        except Exception as e:
            print(f"Selenium/BeautifulSoup failed for {url}: {e}")

    driver.quit()  # Close the browser when done