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
def read_sales(config):
    source_type = config["source_type"]
    field_map = config.get("field_mapping", {})

    if source_type == "CSV":
        return read_from_csv(config["csv_path"], field_map)
    elif source_type == "SQLite":
        return read_from_sqlite(config["sqlite_path"], field_map)
    elif source_type == "MySQL":
        return read_from_mysql(config["mysql"], field_map)
    elif source_type == "API":
        return read_from_api(config["api_url"], field_map, config.get("api_token"))
    else:
        raise ValueError("Unsupported source type")