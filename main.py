from app.scraper import scrape_sources
from app.analyzer import analyze_all
from app.db import get_articles_by_date
from s3_upload import upload_to_s3
from datetime import datetime

#This is the main entry point for the RotaryRadar.AI pipeline
#Feedback for steps in the pipeline is printed to the console
#Make sure to set the OPENAI_API_KEY environment variable before running

if __name__ == "__main__":
    print("Starting RotaryRadar.AI  #serviceaboveself")
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    today_filename = datetime.now().strftime('%Y%m%d')
    
    # Scrape and analyze
    scrape_sources()
    analyze_all()
    
    # Get today's articles from database
    articles = get_articles_by_date(today)
    
    # Format articles for S3 upload
    formatted_articles = []
    for article in articles:
        formatted_articles.append({
            'title': article['title'],
            'url': article['url'],
            'source': article['source'],
            'snippet': article['content'][:300] + '...' if len(article['content']) > 300 else article['content'],
            'ai_suggestion': article.get('gpt_suggestion')
        })
    
    print(f"\n📊 Found {len(formatted_articles)} articles for {today}")
    
    # Upload to S3
    try:
        upload_to_s3(today_filename, formatted_articles)
    except Exception as e:
        print(f"❌ S3 upload failed: {e}")
    
    print("Success! Check http://127.0.0.1:5000 or run export.html.py for a html print out for new articles and GPT suggestions.")