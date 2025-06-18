CREATE TABLE IF NOT EXISTS content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT,
    source TEXT,
    content TEXT,
    is_opportunity INTEGER,
    raw_content TEXT,
    gpt_suggestion TEXT
);