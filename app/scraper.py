from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from .db import insert_article
import os
import time
import openai
import yaml
from app.day_url_limit import filter_urls_last_7_days  # adjust import as needed

#to use OpenAI's GPT-4.1 model for analysis; prompt engineering to get relevant suggestions
def analyze_with_gpt(content):
    prompt = f'Please review the following recent news from Gurnee, Waukegan, and Lake County, IL. Based on current events and community needs, identify and recommend at least two Rotary service or fundraising opportunities that align with Rotary’s areas of focus (e.g., community health, environment, education, youth). Provide context (with names if possible), potential partners, and next steps. Do not include any sections titled "Other Relevant Opportunities," "Optional Bonus," or "Summary Table." Only provide the two main project ideas with their context, partners, and next steps. Do not add any tables or additional opportunity lists.:\n\n{content}'
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1250
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "GPT analysis failed."

def load_urls(yaml_path="sources.yaml"):
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("urls", []), data.get("full_story_depth1", [])

def scrape_depth1(driver, base_url):
    print(f"Scraping {base_url} for 'Full Story' links...")
    driver.get(base_url)
    time.sleep(2)
    full_story_links = driver.find_elements(By.LINK_TEXT, "Full Story")
    links = [link.get_attribute('href') for link in full_story_links]

    # Filter links to only those within the last 7 days
    recent_links = filter_urls_last_7_days(links)
    if not recent_links:
        print(f"No URLs with dates in the last 7 days for {base_url}")
        return

    print(f"Found {len(recent_links)} 'Full Story' links from the last 7 days for {base_url}")
    for link in recent_links:
        try:
            driver.get(link)
            time.sleep(2)
            article_soup = BeautifulSoup(driver.page_source, "html.parser")
            title = article_soup.title.string if article_soup.title else "No Title"
            content = article_soup.get_text(separator='\n', strip=True)
            raw_content = driver.page_source

            gpt_suggestion = analyze_with_gpt(content)
            dummy_data = {
                'title': title,
                'url': link,
                'source': base_url,
                'content': content,
                'raw_content': raw_content,
                'gpt_suggestion': gpt_suggestion
            }
            try:
                insert_article(**dummy_data)
            except Exception as db_err:
                print(f"Database insert failed for {link}: {db_err}")
        except Exception as e:
            print(f"Failed to process {link}: {e}")

def scrape_sources():
    urls, depth1_urls = load_urls()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    # Only run depth1 scraping for full_story_depth1 URLs
    for url in depth1_urls:
        print(f"Running depth-1 scraping for {url} ...")
        try:
            scrape_depth1(driver, url)
        except Exception as e:
            print(f"Selenium/BeautifulSoup failed for {url}: {e}")

    # Normal scanning logic for URLs under 'urls:'
    for url in urls:
        print(f"Running normal scraping for {url} ...")
        try:
            driver.get(url)
            time.sleep(2)
            article_soup = BeautifulSoup(driver.page_source, "html.parser")
            title = article_soup.title.string if article_soup.title else "No Title"
            content = article_soup.get_text(separator='\n', strip=True)
            raw_content = driver.page_source

            gpt_suggestion = analyze_with_gpt(content)
            dummy_data = {
                'title': title,
                'url': url,
                'source': url,
                'content': content,
                'raw_content': raw_content,
                'gpt_suggestion': gpt_suggestion
            }
            try:
                insert_article(**dummy_data)
            except Exception as db_err:
                print(f"Database insert failed for {url}: {db_err}")
        except Exception as e:
            print(f"Failed to process {url}: {e}")

    driver.quit()