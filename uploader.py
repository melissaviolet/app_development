import firebase_admin
from firebase_admin import credentials, firestore
import os
import datetime

# Load Firebase service account
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def send_sales_to_firebase(sales_data, store_id="default_store"):
    """
    sales_data = List of dicts:
    [
      {"product_id": "A123", "name": "Milk", "qty": 2, "price": 4500, "timestamp": "2024-07-07T13:00:00"},
      ...
    ]
    """
    store_ref = db.collection("sales").document(store_id)
    batch_ref = store_ref.collection("batches").document(datetime.datetime.now().isoformat())
    batch_ref.set({"uploaded": True, "count": len(sales_data)})

    for sale in sales_data:
        batch_ref.collection("items").add(sale)

    print(f"✅ Uploaded {len(sales_data)} sales to Firestore.")
