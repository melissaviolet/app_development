import sqlite3

def read_sales_from_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, qty, price, timestamp FROM sales")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"name": row[0], "qty": row[1], "price": float(row[2]), "timestamp": row[3]} for row in rows
        for row in rows
    ]
