from flask import Flask, render_template
import sqlite3
import os
import markdown

app = Flask(__name__)

DB_PATH = 'rotary.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        source TEXT,
        content TEXT,
        is_opportunity INTEGER,
        raw_content TEXT,
        gpt_suggestion TEXT
    )''')
    conn.commit()
    conn.close()

def insert_article(title, url, source, content, raw_content=None, gpt_suggestion=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO content (title, url, source, content, raw_content, gpt_suggestion) VALUES (?, ?, ?, ?, ?, ?)",
        (title, url, source, content, raw_content, gpt_suggestion)
    )
    conn.commit()
    conn.close()

def get_unanalyzed_articles():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM content WHERE is_opportunity IS NULL").fetchall()
    columns = [desc[0] for desc in c.description]
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def update_analysis(article_id, is_opportunity, gpt_suggestion):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE content SET is_opportunity=?, gpt_suggestion=? WHERE id=?",
              (is_opportunity, gpt_suggestion, article_id))
    conn.commit()
    conn.close()

def get_opportunities():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM content").fetchall()
    columns = [desc[0] for desc in c.description]
    conn.close()
    return [dict(zip(columns, row)) for row in rows]


@app.route("/")
def index():
    articles = get_opportunities()
    for article in articles:
        if 'gpt_suggestion' in article:
            article['gpt_suggestion_html'] = markdown.markdown(article['gpt_suggestion'])
    return render_template("index.html", rows=articles)

if __name__ == "__main__": 
    app.run(debug=True)