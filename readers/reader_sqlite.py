import sqlite3

def read_sales_from_sqlite(file_path):
    conn = sqlite3.connect(file_path)
    cur = conn.cursor()
    cur.execute("SELECT product_id, name, qty, price, timestamp FROM sales")
    rows = cur.fetchall()
    conn.close()
    return [
        {"product_id": r[0], "name": r[1], "qty": r[2], "price": r[3], "timestamp": r[4]}
        for r in rows
    ]