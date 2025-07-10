import requests

def read_sales_from_api(api_url, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")