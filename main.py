from app.scraper import scrape_sources
from app.analyzer import analyze_all

#This is the main entry point for the RotaryRadar.AI pipeline
#Feedback for steps in the pipeline is printed to the console
#Make sure to set the OPENAI_API_KEY environment variable before running

if __name__ == "__main__":
    print("Starting RotaryRadar.AI  #serviceaboveself")
    scrape_sources()
    analyze_all()
    print("Success! Check http://127.0.0.1:5000 or run export.html.py for a html print out for new articles and GPT suggestions.")