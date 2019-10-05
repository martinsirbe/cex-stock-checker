import requests
import yaml

CEX_API_STORES_LOOKUP_URL = "https://wss2.cex.uk.webuy.io/v3/stores"


# Make a get request to CEX to obtain all stores
def get_stores():
    return requests.get(CEX_API_STORES_LOOKUP_URL).json()["response"]["data"]["stores"]


stores = {}
for store in get_stores():
    stores[store.get("storeId")] = store.get("storeName")

with open('config/stores.yaml', 'w') as f:
    data = yaml.dump(stores, f)
