from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from .db import insert_article
import os
import time
import openai
import yaml
import feedparser

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

def load_sources(yaml_path="sources.yaml"):
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    urls = data.get("urls", [])
    full_story_depth1 = data.get("full_story_depth1", [])
    rss_feeds = data.get("rss_feeds", [])
    return urls, full_story_depth1, rss_feeds

def process_rss_feed(feed_url):
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        title = entry.get('title', 'No Title')
        url = entry.get('link', '')
        summary = entry.get('summary', '')
        content = summary  # Or fetch the full article if needed
        gpt_suggestion = analyze_with_gpt(content)
        dummy_data = {
            'title': title,
            'url': url,
            'source': feed_url,
            'content': content,
            'raw_content': summary,
            'gpt_suggestion': gpt_suggestion
        }
        try:
            insert_article(**dummy_data)
        except Exception as db_err:
            print(f"Database insert failed for {url}: {db_err}")

def scrape_depth1(driver, url):
    print(f"Executing depth-1 scrape for {url}")
    driver.get(url)
    time.sleep(2)
    # Find all "Full Story" links
    full_story_links = driver.find_elements(By.LINK_TEXT, "Full Story")
    links = [link.get_attribute('href') for link in full_story_links]

    for link in links:
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
                'source': url,
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

    # Optionally, return to the main page if you want to do more
    driver.get(url)

def scrape_sources():
    urls, full_story_depth1, rss_feeds = load_sources()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    # Debug print to confirm full_story_depth1 URLs are loaded
    print("full_story_depth1 URLs:", full_story_depth1)

    # Normal URLs
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

    # Full Story Depth 1 URLs
    for url in full_story_depth1:
        print(f"Scraping {url} for 'Full Story' links...")
        scrape_depth1(driver, url)

    # RSS feeds
    for feed_url in rss_feeds:
        print(f"Processing RSS feed: {feed_url}")
        process_rss_feed(feed_url)

    driver.quit()