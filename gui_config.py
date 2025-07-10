import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

CONFIG_FILE = "config.json"

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def get_store_id():
    config = load_config()
    return config.get("store_id", "")

def set_store_id(store_id):
    config = load_config()
    config["store_id"] = store_id
    save_config(config)

def launch_config_gui():
    def on_save():
        store_id = store_id_var.get().strip()
        pos_type = pos_type_var.get()

        if not store_id:
            messagebox.showwarning("Missing Store ID", "Please enter your store ID.")
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
        messagebox.showinfo("Success", "Configuration saved successfully!")
        root.destroy()

    def choose_file(var):
        filename = filedialog.askopenfilename()
        var.set(filename)

    root = tk.Tk()
    root.title("Connector Setup")
    root.geometry("400x400")

    # Variables
    store_id_var = tk.StringVar(value=get_store_id())
    pos_type_var = tk.StringVar()
    csv_path_var = tk.StringVar()
    sqlite_path_var = tk.StringVar()
    host_var = tk.StringVar()
    user_var = tk.StringVar()
    pass_var = tk.StringVar()
    db_var = tk.StringVar()
    api_url_var = tk.StringVar()
    api_token_var = tk.StringVar()

    # UI
    ttk.Label(root, text="Store ID").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    ttk.Entry(root, textvariable=store_id_var).grid(row=0, column=1, padx=5)

    ttk.Label(root, text="POS Source Type").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    ttk.Combobox(root, textvariable=pos_type_var, values=["csv", "sqlite", "mysql", "api"]).grid(row=1, column=1, padx=5)

    ttk.Label(root, text="CSV File").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    ttk.Entry(root, textvariable=csv_path_var).grid(row=2, column=1, padx=5)
    ttk.Button(root, text="Browse", command=lambda: choose_file(csv_path_var)).grid(row=2, column=2, padx=5)

    ttk.Label(root, text="SQLite File").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    ttk.Entry(root, textvariable=sqlite_path_var).grid(row=3, column=1, padx=5)
    ttk.Button(root, text="Browse", command=lambda: choose_file(sqlite_path_var)).grid(row=3, column=2, padx=5)

    ttk.Label(root, text="MySQL Host").grid(row=4, column=0, sticky="w", padx=5)
    ttk.Entry(root, textvariable=host_var).grid(row=4, column=1, padx=5)
    ttk.Label(root, text="MySQL User").grid(row=5, column=0, sticky="w", padx=5)
    ttk.Entry(root, textvariable=user_var).grid(row=5, column=1, padx=5)
    ttk.Label(root, text="MySQL Pass").grid(row=6, column=0, sticky="w", padx=5)
    ttk.Entry(root, textvariable=pass_var, show="*").grid(row=6, column=1, padx=5)
    ttk.Label(root, text="MySQL DB").grid(row=7, column=0, sticky="w", padx=5)
    ttk.Entry(root, textvariable=db_var).grid(row=7, column=1, padx=5)

    ttk.Label(root, text="API URL").grid(row=8, column=0, sticky="w", padx=5)
    ttk.Entry(root, textvariable=api_url_var).grid(row=8, column=1, padx=5)
    ttk.Label(root, text="API Token").grid(row=9, column=0, sticky="w", padx=5)
    ttk.Entry(root, textvariable=api_token_var).grid(row=9, column=1, padx=5)

    ttk.Button(root, text="Save Config", command=on_save).grid(row=10, column=1, pady=15)

    root.mainloop()

# For direct testing
if __name__ == "__main__":
    launch_config_gui()
