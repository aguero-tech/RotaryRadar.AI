import sqlite3
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import markdown
import os

DB_PATH = 'rotary.db'
TEMPLATE_PATH = 'templates'
TEMPLATE_FILE = 'summary.html'
EXPORT_DIR = 'exports'

def export_today_summary():
    today = datetime.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM content WHERE scan_date = ?", (today,)).fetchall()
    columns = [desc[0] for desc in c.description]
    conn.close()
    if not rows:
        print("No entries for today.")
        return

    data = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        # If gpt_suggestion_html is empty but gpt_suggestion exists, convert it to HTML
        if not row_dict.get('gpt_suggestion_html') and row_dict.get('gpt_suggestion'):
            row_dict['gpt_suggestion_html'] = markdown.markdown(row_dict['gpt_suggestion'])
        data.append(row_dict)

    env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
    template = env.get_template(TEMPLATE_FILE)
    output_html = template.render(rows=data)
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
    output_filename = os.path.join(EXPORT_DIR, f"{today.replace('-', '')}.html")
    with open(output_filename, "w") as f:
        f.write(output_html)
    print(f"Exported today's summary to {output_filename}")

def generate_index_html(directory=EXPORT_DIR):
    files = sorted(
        f for f in os.listdir(directory)
        if f.endswith('.html') and f != 'index.html' and f != 'weekly_impact_summary.html'
    )
    with open(os.path.join(directory, 'index.html'), 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Rotary Summaries Index</title></head><body>\n')
        f.write('<h1>Rotary Daily Summaries</h1>\n<ul>\n')
        for file in files:
            date_str = file.replace('.html', '')
            f.write(f'<li><a href="{file}">{date_str}</a></li>\n')
        f.write('</ul>\n</body></html>')
    print("Exported today's index.html to exports/index.html")

if __name__ == "__main__":
    export_today_summary()
    generate_index_html()