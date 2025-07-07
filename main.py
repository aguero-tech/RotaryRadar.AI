from app.scraper import scrape_sources
from app.analyzer import analyze_all
from dotenv import load_dotenv
import subprocess

#This is the main entry point for the RotaryRadar.AI pipeline
#Feedback for steps in the pipeline is printed to the console
#Make sure to set the OPENAI_API_KEY environment variable before running

if __name__ == "__main__":
    load_dotenv()
    print("Starting RotaryRadar.AI  #serviceaboveself")
    scrape_sources()
    analyze_all()
    print("Exporting today's summary and index...")
    subprocess.run(["python", "export.today.html.py"], check=True)
    print("Uploading to S3...")
    subprocess.run(["python", "upload.to.s3.py"], check=True)
    print("Success! Check http://127.0.0.1:5000 or your S3 bucket for the latest HTML exports.")