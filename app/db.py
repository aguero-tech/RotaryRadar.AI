import sqlite3

DB_PATH = 'rotary.db'

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