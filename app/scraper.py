from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from .db import insert_article
import os
import time
import openai
import yaml

#to use OpenAI's GPT-4.1 model for analysis; prompt engineering to get relevant suggestions
def analyze_with_gpt(content):
    prompt = f"Please review the following recent news from Gurnee, Waukegan, and Lake County, IL. Based on current events and community needs, identify and recommend at least two Rotary service or fundraising opportunities that align with Rotary’s areas of focus (e.g., community health, environment, education, youth). Provide context, potential partners, and next steps.:\n\n{content}"
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "GPT analysis failed."

def load_urls(yaml_path="sources.yaml"):
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("urls", [])

def scrape_sources():
    urls = load_urls()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    for url in urls:
        print(f"Scraping {url} for current articles...")
        try:
            driver.get(url)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            content = soup.get_text(separator='\n', strip=True)
            raw_content = driver.page_source
            title = soup.title.string if soup.title else "No Title"
            print(f"Title: {title}\nContent: {content[:250]}...\n")

            gpt_suggestion = analyze_with_gpt(content)

            dummy_data = {
                'title': title,
                'url': url,
                'source': 'Daily Herald',
                'content': content,
                'raw_content': raw_content,
                'gpt_suggestion': gpt_suggestion
            }
            try:
                insert_article(**dummy_data)
            except Exception as db_err:
                print(f"Database insert failed for {url}: {db_err}")

        except Exception as e:
            print(f"Selenium/BeautifulSoup failed for {url}: {e}")

    driver.quit()