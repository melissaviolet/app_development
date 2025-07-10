import csv

def read_sales_from_csv(file_path):
    sales = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["qty"] = int(row["qty"])
            row["price"] = float(row["price"])
            sales.append(row)
    return sales