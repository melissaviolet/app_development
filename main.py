from gui_config import launch_config_gui, get_store_id
from reader_dispatcher import read_sales
from uploader import send_sales_to_firebase
from config_manager import load_config

def main():
    config = load_config()

    # If config or store_id missing, launch setup GUI
    if not config or not config.get("store_id"):
        launch_config_gui()
        config = load_config()  # reload after GUI save

    store_id = config.get("store_id")
    if not store_id:
        print("❌ Store ID is required. Please run setup again.")
        return

    print(f"Using store ID: {store_id}")
    print(f"Using POS source: {config.get('source_type')}")

    # read_sales should read config internally or accept config to read correct source
    sales = read_sales(config)
    if not sales:
        print("❌ No sales data found.")
        return

    send_sales_to_firebase(sales, store_id=store_id)
    print("✅ Sales upload complete.")

if __name__ == "__main__":
    main()
