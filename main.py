from app.scraper import scrape_sources
from app.analyzer import analyze_all

if __name__ == "__main__":
    print("Starting RotaryRadar.AI pipeline...")
    scrape_sources()
    analyze_all()
    print("Pipeline complete.")