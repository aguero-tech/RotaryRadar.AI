from .db import get_unanalyzed_articles, update_analysis

def analyze_all():
    print("Analyzing articles...")
    for article in get_unanalyzed_articles():
        suggestion = article.get('gpt_suggestion')
        if suggestion and suggestion != "GPT analysis failed.":
            update_analysis(article['id'], 1, suggestion)
        else:
            update_analysis(article['id'], 0, 'No opportunity detected.')
