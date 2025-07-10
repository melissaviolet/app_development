import mysql.connector

def read_sales_from_mysql(config):
    conn = mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )
    cur = conn.cursor()
    cur.execute("SELECT product_id, name, qty, price, timestamp FROM sales")
    rows = cur.fetchall()
    conn.close()
    return [
        {"product_id": r[0], "name": r[1], "qty": r[2], "price": float(r[3]), "timestamp": r[4]}
        for r in rows
    ]