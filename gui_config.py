import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

CONFIG_FILE = "config.json"

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def launch_config_gui():
    def on_save():
        store_id = store_id_var.get().strip()
        pos_type = pos_type_var.get()

        if not store_id or not pos_type:
            messagebox.showerror("Error", "Store ID and POS Source Type are required.")
            return

        config = {
            "store_id": store_id,
            "source_type": pos_type
        }

        if pos_type == "csv":
            config["csv"] = {"file_path": csv_path_var.get()}
        elif pos_type == "sqlite":
            config["sqlite"] = {"file_path": sqlite_path_var.get()}
        elif pos_type == "mysql":
            config["mysql"] = {
                "host": host_var.get(),
                "user": user_var.get(),
                "password": pass_var.get(),
                "database": db_var.get()
            }
        elif pos_type == "api":
            config["api"] = {
                "url": api_url_var.get(),
                "token": api_token_var.get()
            }

        save_config(config)
        messagebox.showinfo("Saved", "Configuration saved successfully!")
        root.destroy()

    def choose_file(var):
        filename = filedialog.askopenfilename()
        var.set(filename)

    def show_fields(*args):
        # Hide all fields
        for frame in all_frames:
            frame.grid_remove()

        selected = pos_type_var.get()
        if selected == "csv":
            csv_frame.grid(row=2, column=0, columnspan=3, pady=2)
        elif selected == "sqlite":
            sqlite_frame.grid(row=3, column=0, columnspan=3, pady=2)
        elif selected == "mysql":
            mysql_frame.grid(row=4, column=0, columnspan=3, pady=2)
        elif selected == "api":
            api_frame.grid(row=5, column=0, columnspan=3, pady=2)

    # GUI Window
    root = tk.Tk()
    root.title("Connector Setup")

    store_id_var = tk.StringVar()
    pos_type_var = tk.StringVar()
    csv_path_var = tk.StringVar()
    sqlite_path_var = tk.StringVar()
    host_var = tk.StringVar()
    user_var = tk.StringVar()
    pass_var = tk.StringVar()
    db_var = tk.StringVar()
    api_url_var = tk.StringVar()
    api_token_var = tk.StringVar()

    ttk.Label(root, text="Store ID").grid(row=0, column=0, pady=5)
    ttk.Entry(root, textvariable=store_id_var).grid(row=0, column=1)

    ttk.Label(root, text="POS Source Type").grid(row=1, column=0, pady=5)
    pos_dropdown = ttk.Combobox(root, textvariable=pos_type_var, values=["csv", "sqlite", "mysql", "api"])
    pos_dropdown.grid(row=1, column=1)
    pos_dropdown.bind("<<ComboboxSelected>>", show_fields)

    # CSV
    csv_frame = ttk.Frame(root)
    ttk.Label(csv_frame, text="CSV File").grid(row=0, column=0)
    ttk.Entry(csv_frame, textvariable=csv_path_var).grid(row=0, column=1)
    ttk.Button(csv_frame, text="Browse", command=lambda: choose_file(csv_path_var)).grid(row=0, column=2)

    # SQLite
    sqlite_frame = ttk.Frame(root)
    ttk.Label(sqlite_frame, text="SQLite File").grid(row=0, column=0)
    ttk.Entry(sqlite_frame, textvariable=sqlite_path_var).grid(row=0, column=1)
    ttk.Button(sqlite_frame, text="Browse", command=lambda: choose_file(sqlite_path_var)).grid(row=0, column=2)

    # MySQL
    mysql_frame = ttk.Frame(root)
    ttk.Label(mysql_frame, text="MySQL Host").grid(row=0, column=0)
    ttk.Entry(mysql_frame, textvariable=host_var).grid(row=0, column=1)
    ttk.Label(mysql_frame, text="MySQL User").grid(row=1, column=0)
    ttk.Entry(mysql_frame, textvariable=user_var).grid(row=1, column=1)
    ttk.Label(mysql_frame, text="MySQL Pass").grid(row=2, column=0)
    ttk.Entry(mysql_frame, textvariable=pass_var, show="*").grid(row=2, column=1)
    ttk.Label(mysql_frame, text="MySQL DB").grid(row=3, column=0)
    ttk.Entry(mysql_frame, textvariable=db_var).grid(row=3, column=1)

    # API
    api_frame = ttk.Frame(root)
    ttk.Label(api_frame, text="API URL").grid(row=0, column=0)
    ttk.Entry(api_frame, textvariable=api_url_var).grid(row=0, column=1)
    ttk.Label(api_frame, text="API Token").grid(row=1, column=0)
    ttk.Entry(api_frame, textvariable=api_token_var).grid(row=1, column=1)

    all_frames = [csv_frame, sqlite_frame, mysql_frame, api_frame]

    ttk.Button(root, text="Save Config", command=on_save).grid(row=10, column=1, pady=15)

    root.mainloop()
