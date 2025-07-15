import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CONFIG_FILE = "config.json"

def launch_config_gui():
    def save_config():
        config = {
            "source_type": source_var.get(),
            "store_id": store_id_entry.get(),
            "field_mapping": {
                "name": name_entry.get(),
                "qty": qty_entry.get(),
                "price": price_entry.get(),
                "timestamp": timestamp_entry.get(),
            }
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

        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)

        messagebox.showinfo("Saved", "Configuration saved successfully!")
        root.destroy()

    def show_fields(*args):
        source = source_var.get()
        csv_frame.pack_forget()
        sqlite_frame.pack_forget()
        mysql_frame.pack_forget()
        api_frame.pack_forget()

        if source == "CSV":
            csv_frame.pack(fill="x")
        elif source == "SQLite":
            sqlite_frame.pack(fill="x")
        elif source == "MySQL":
            mysql_frame.pack(fill="x")
        elif source == "API":
            api_frame.pack(fill="x")

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

    # 🔑 Field Mapping Section
    tk.Label(root, text="\nField Mapping (match your column names)").pack()
    tk.Label(root, text="Product Name Column:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    tk.Label(root, text="Quantity Column:").pack()
    qty_entry = tk.Entry(root)
    qty_entry.pack()

    tk.Label(root, text="Price Column:").pack()
    price_entry = tk.Entry(root)
    price_entry.pack()

    tk.Label(root, text="Timestamp Column:").pack()
    timestamp_entry = tk.Entry(root)
    timestamp_entry.pack()

    # Save Button
    tk.Button(root, text="Save Configuration", command=save_config).pack(pady=10)

    root.mainloop()
