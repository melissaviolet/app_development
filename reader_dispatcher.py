from readers.reader_csv import read_sales_from_csv
from readers.reader_sqlite import read_sales_from_sqlite
from readers.reader_mysql import read_sales_from_mysql
from readers.reader_api import read_sales_from_api

def read_sales(config):
    src = config.get("source_type")
    if src == "csv":
        return read_sales_from_csv(config["csv"]["file_path"])
    elif src == "sqlite":
        return read_sales_from_sqlite(config["sqlite"]["file_path"])
    elif src == "mysql":
        return read_sales_from_mysql(config["mysql"])
    elif src == "api":
        return read_sales_from_api(config["api"]["url"], config["api"].get("token"))
    else:
        raise ValueError("Unsupported source type")
