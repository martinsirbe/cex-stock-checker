import sys
import html
import random
import re
from time import sleep

import requests

MAX_DELAY = 3
MIN_DELAY = 2
LAST_STORE_ID = 350
STORES_YAML = 'stores.yaml'
STORE_URL = 'https://uk.webuy.com/stores/store_details.php?branchId={}'
FINISH_MSG = 'Finished updating stores YAML file.'

stores_yaml = 'stores:\n'
storeId = 1

while storeId <= LAST_STORE_ID:
    response = requests.get(STORE_URL.format(storeId))

    match = re.search('<h3>(.*)</h3>', response.text)
    shop_name_h3_element = match.group(0)

    shop_name = shop_name_h3_element.replace('<h3>', '').replace('</h3>', '')
    shop_name = html.unescape(shop_name)
    if shop_name != 'Find your local CeX shop' and shop_name != '':
        print('Adding store to list: ' + shop_name)
        stores_yaml += '  ' + str(storeId) + ': "' + shop_name + '"\n'

    sleep(float(random.uniform(MIN_DELAY, MAX_DELAY)))
    storeId += 1

    text_file = open(STORES_YAML, 'w')
    text_file.write(stores_yaml)
    text_file.close()
sys.exit(FINISH_MSG)
