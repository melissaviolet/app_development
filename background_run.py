import os
import winreg
from reader_dispatcher import read_sales
from uploader import send_sales_to_firebase
from config_manager import load_config, get_store_id
from logger import log_sync

def add_to_startup(exe_path=None):
    if exe_path is None:
        exe_path = os.path.abspath(__file__)
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    reg_key = winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(reg_key, "FreshTallyConnector", 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(reg_key)

# Run once to add the app to startup
add_to_startup()

# Main background task
try:
    config = load_config()
    sales = read_sales(config)
    store_id = get_store_id()
    
    send_sales_to_firebase(sales, store_id)
    
    log_sync("success", store_id, record_count=len(sales))

except Exception as e:
    store_id = get_store_id()
    log_sync("failure", store_id, error=str(e))
