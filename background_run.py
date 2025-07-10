from reader_dispatcher import read_sales
from uploader import send_sales_to_firebase
from config_manager import get_store_id
from logger import log_sync

try:
    sales = read_sales()
    store_id = get_store_id()
    send_sales_to_firebase(sales, store_id)
    log_sync(success=True)
except Exception as e:
    log_sync(success=False, error=str(e))
