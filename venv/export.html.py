import sqlite3
import os

DB_PATH = 'rotary.db'
RESULTS_DIR = os.path.join('app', 'results')
HTML_PATH = os.path.join(RESULTS_DIR, 'opportunities.html')

def export_to_html(html_path=HTML_PATH):
    # Ensure the results directory exists
    os.makedirs(os.path.dirname(html_path), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM content").fetchall()
    columns = [desc[0] for desc in c.description]
    conn.close()

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Opportunities</title></head><body>\n')
        f.write('<h1>Opportunities</h1>\n')
        f.write('<table border="1">\n<tr>')
        for col in columns:
            f.write(f'<th>{col}</th>')
        f.write('</tr>\n')
        for row in rows:
            f.write('<tr>')
            for cell in row:
                f.write(f'<td>{cell}</td>')
            f.write('</tr>\n')
        f.write('</table>\n</body></html>')
    print(f"Exported to {html_path}")

if __name__ == "__main__":
    export_to_html()