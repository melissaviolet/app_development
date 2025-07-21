import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import csv
import sqlite3
import requests

CONFIG_FILE = "config.json"

def launch_config_gui():
    def save_config():
        config = {
            "source_type": source_var.get(),
            "store_id": store_id_entry.get(),
            "field_mapping": {field: var.get() for field, var in field_vars.items()}
        }

        # Add POS-specific fields
        if config["source_type"] == "CSV":
            config["csv_path"] = csv_path_entry.get()
        elif config["source_type"] == "SQLite":
            config["sqlite_path"] = sqlite_path_entry.get()
        elif config["source_type"] == "MySQL":
            config["mysql"] = {
                "host": host_entry.get(),
                "user": user_entry.get(),
                "password": password_entry.get(),
                "database": database_entry.get()
            }
        elif config["source_type"] == "API":
            config["api_url"] = api_url_entry.get()

        missing_fields = [label for field, label in field_labels.items() if not field_vars[field].get()]
        if missing_fields:
            messagebox.showwarning("Missing Fields", f"Please map all required fields:\n\n{chr(10).join(missing_fields)}")
            return

        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)

        messagebox.showinfo("Saved", "Configuration saved successfully!")
        root.destroy()

    def show_fields(*args):
        csv_frame.pack_forget()
        sqlite_frame.pack_forget()
        mysql_frame.pack_forget()
        api_frame.pack_forget()
        source = source_var.get()
        if source == "CSV":
            csv_frame.pack(fill="x")
        elif source == "SQLite":
            sqlite_frame.pack(fill="x")
        elif source == "MySQL":
            mysql_frame.pack(fill="x")
        elif source == "API":
            api_frame.pack(fill="x")

    def detect_columns_and_populate():
        try:
            source_type = source_var.get()
            columns = []

            if source_type == "CSV":
                path = csv_path_entry.get()
                if not os.path.exists(path):
                    raise Exception("CSV file not found.")
                with open(path, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    columns = reader.fieldnames or []
            elif source_type == "SQLite":
                path = sqlite_path_entry.get()
                if not os.path.exists(path):
                    raise Exception("SQLite DB file not found.")
                conn = sqlite3.connect(path)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                if not tables:
                    raise Exception("No tables found in SQLite DB.")
                # Try to get columns from the first table
                table_name = tables[0][1]
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = [row[1] for row in cursor.fetchall()]
                conn.close()
            elif source_type == "MySQL":
                import mysql.connector
                conn = mysql.connector.connect(
                    host=host_entry.get(),
                    user=user_entry.get(),
                    password=password_entry.get(),
                    database=database_entry.get()
                )
                cursor = conn.cursor()
                cursor.execute("SHOW TABLES;")
                tables = cursor.fetchall()
                if not tables:
                    raise Exception("No tables found in MySQL DB.")
                table_name = tables[0][0]
                cursor.execute(f"DESCRIBE {table_name};")
                columns = [row[0] for row in cursor.fetchall()]
                conn.close()
            elif source_type == "API":
                url = api_url_entry.get()
                response = requests.get(url)
                if response.status_code == 200:
                    sample = response.json()
                    if isinstance(sample, list) and len(sample) > 0:
                        columns = list(sample[0].keys())
                else:
                    raise Exception(f"API request failed: {response.status_code}")

            if not columns:
                raise Exception("No columns detected.")

            for var in field_vars.values():
                var.set("")  # clear old value
            for field, dropdown in field_dropdowns.items():
                dropdown.config(values=columns)

        except Exception as e:
            messagebox.showerror("Error detecting columns", str(e))

    root = tk.Tk()
    root.title("Connector Configuration")

    tk.Label(root, text="Select Source Type:").pack()
    source_var = tk.StringVar()
    source_dropdown = ttk.Combobox(root, textvariable=source_var, values=["CSV", "SQLite", "MySQL", "API"])
    source_dropdown.bind("<<ComboboxSelected>>", show_fields)
    source_dropdown.pack()

    # Store ID
    tk.Label(root, text="Store ID:").pack()
    store_id_entry = tk.Entry(root)
    store_id_entry.pack()

    # Source-specific fields
    csv_frame = tk.Frame(root)
    tk.Label(csv_frame, text="CSV File Path:").pack()
    csv_path_entry = tk.Entry(csv_frame)
    csv_path_entry.pack()

    sqlite_frame = tk.Frame(root)
    tk.Label(sqlite_frame, text="SQLite DB Path:").pack()
    sqlite_path_entry = tk.Entry(sqlite_frame)
    sqlite_path_entry.pack()

    mysql_frame = tk.Frame(root)
    tk.Label(mysql_frame, text="MySQL Host:").pack()
    host_entry = tk.Entry(mysql_frame)
    host_entry.pack()
    tk.Label(mysql_frame, text="User:").pack()
    user_entry = tk.Entry(mysql_frame)
    user_entry.pack()
    tk.Label(mysql_frame, text="Password:").pack()
    password_entry = tk.Entry(mysql_frame, show="*")
    password_entry.pack()
    tk.Label(mysql_frame, text="Database:").pack()
    database_entry = tk.Entry(mysql_frame)
    database_entry.pack()

    api_frame = tk.Frame(root)
    tk.Label(api_frame, text="API URL:").pack()
    api_url_entry = tk.Entry(api_frame)
    api_url_entry.pack()

    # Field Mapping Section
    tk.Label(root, text="\nField Mapping (match your column names)").pack()
    mapping_frame = tk.Frame(root)
    mapping_frame.pack(fill="x", padx=10, pady=2)

    field_labels = {
        "product_id": "Product ID Field",
        "name": "Product Name Field",
        "qty": "Quantity Field",
        "price": "Price Field",
        "timestamp": "Timestamp Field"
    }

    field_vars = {}
    field_dropdowns = {}
    for i, (field, label) in enumerate(field_labels.items()):
        row = tk.Frame(mapping_frame)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=label, width=20, anchor="w").pack(side="left")
        var = tk.StringVar()
        dropdown = ttk.Combobox(row, textvariable=var, values=[], state="normal")
        dropdown.pack(side="left", fill="x", expand=True)
        field_vars[field] = var
        field_dropdowns[field] = dropdown

    # Detect Columns Button
    tk.Button(root, text="Detect Columns", command=detect_columns_and_populate).pack(pady=5)

    # Save Button
    tk.Button(root, text="Save Configuration", command=save_config).pack(pady=10)

    root.mainloop()