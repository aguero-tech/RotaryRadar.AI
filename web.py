import sqlite3

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
    result = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        # Convert is_opportunity: 1 -> 'yes', 0 -> 'no', None stays None
        if row_dict.get('is_opportunity') == 1:
            row_dict['is_opportunity'] = 'yes'
        elif row_dict.get('is_opportunity') == 0:
            row_dict['is_opportunity'] = 'no'
        result.append(row_dict)
    conn.close()
    return result
