import sqlite3
from datetime import datetime, timedelta
import openai
import os
from jinja2 import Environment, FileSystemLoader
import markdown

DB_PATH = 'rotary.db'

def get_recent_articles(days=7):
    print("Connecting to database and fetching recent articles...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    week_ago = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
    rows = c.execute("SELECT * FROM content WHERE scan_date >= ?", (week_ago,)).fetchall()
    columns = [desc[0] for desc in c.description]
    conn.close()
    print(f"Found {len(rows)} articles from the last {days} days.")
    return [dict(zip(columns, row)) for row in rows]

def analyze_with_gpt(prompt):
    print("Sending combined content to GPT for collective analysis...")
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        print("Received response from GPT.")
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "GPT analysis failed."

def generate_weekly_summary_html(gpt_summary, output_path="weekly_impact_summary.html"):
    print(f"Generating HTML summary at {output_path} ...")
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('weekly_summary.html')
    with open(output_path, "w") as f:
        f.write(template.render(summary=gpt_summary))
    print("HTML summary generated.")

def main():
    print("Starting weekly summary generation...")
    articles = get_recent_articles(days=7)
    # Collect all gpt_suggestion_html or fallback to content
    collected = []
    for idx, article in enumerate(articles, 1):
        suggestion = article.get('gpt_suggestion_html') or article.get('gpt_suggestion') or article.get('content')
        if suggestion:
            collected.append(f"Article {idx}:\n{suggestion}\n")
    if not collected:
        print("No content found for the last 7 days.")
        return

    # Compose a single prompt for GPT
    combined_content = "\n\n".join(collected)
    prompt = (
        "You are helping a local Rotary Club identify the most impactful ways to serve their community based on the following summaries from the past week.\n\n"
        "Please review all the following suggestions and:\n"
        "1. Identify the most pressing community needs, challenges, or concerns that appear across these articles.\n"
        "2. Suggest the top 2-3 realistic, high-impact volunteer opportunities or actions Rotary members can take that address these needs collectively.\n"
        "3. Explain why these actions matter and how they address the needs.\n"
        "4. Keep suggestions practical, creative, and appropriate for a civic or nonprofit group.\n\n"
        "Here are the summaries:\n\n"
        f"{combined_content}"
    )
    gpt_summary = analyze_with_gpt(prompt)

    # Convert GPT summary from Markdown to HTML
    gpt_summary_html = markdown.markdown(gpt_summary)

    # Generate HTML summary using the converted HTML
    generate_weekly_summary_html(gpt_summary_html)
    print("Done.")

if __name__ == "__main__":
    main()
