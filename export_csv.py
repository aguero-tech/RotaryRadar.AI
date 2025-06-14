import sqlite3
import csv

DB_PATH = 'rotary.db'

def export_to_csv(csv_path='opportunities.csv'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM content").fetchall()
    columns = [desc[0] for desc in c.description]
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
    conn.close()
    print(f"Exported to {csv_path}")

if __name__ == "__main__":
    export_to_csv()