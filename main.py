import tkinter as tk
from tkinter import messagebox
from gui_config import launch_config_gui
from reader_dispatcher import read_sales
from uploader import send_sales_to_firebase
from config_manager import load_config

def main():
    # Show configuration GUI if config.json doesn't exist
    try:
        config = load_config()
    except Exception:
        launch_config_gui()
        config = load_config()

    try:
        sales = read_sales()
        send_sales_to_firebase(sales, config["store_id"])

        # ✅ Show success popup
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Success", f"Uploaded {len(sales)} sales records for store: {config['store_id']}")

    except Exception as e:
        # ❌ Show error popup
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Upload Failed", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    main()
