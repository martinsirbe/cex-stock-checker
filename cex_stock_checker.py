import yaml
import requests
from time import sleep

OUT_OF_STOCK = "Out Of Stock"

INPUT_YES = "y"
INPUT_NO = "n"

CONFIG_YAML = "config.yaml"
CONFIG_REQUEST_DELAY = "requestDelay"
CONFIG_ITEMS = "items"

CHECK_URL = "https://uk.webuy.com/product.php?sku={}#."
PROCEED_PROMPT_MSG = "Do you wish to continue to check the stock for {} items? (y/n)"
OUT_OF_STOCK_MSG = "Item with ID {} is currently out of stock."
IN_STOCK_MSG = "Item with ID {} is in stock."
ABORT_MSG = "Aborting the stock check."
WRONG_INPUT_MSG = "Sorry, I didn't get that, please choose either y or n"
ITEM_COUNT_MSG = "Currently there are {} items in your check list."


def check_stock(proceed):
    if proceed == INPUT_YES:
        for item in items_to_check:
            sleep(float(request_delay))
            item_id = str(item)
            response = requests.get(CHECK_URL.format(item_id))

            if OUT_OF_STOCK in response.text:
                print(OUT_OF_STOCK_MSG.format(item_id))
            else:
                print(IN_STOCK_MSG.format(item_id))
    elif proceed == INPUT_NO:
        print(ABORT_MSG)
    else:
        print(WRONG_INPUT_MSG)
        check_stock(input(PROCEED_PROMPT_MSG.format(item_count)))


with open(CONFIG_YAML, "r") as stream:
    try:
        config = yaml.load(stream)
        items_to_check = config[CONFIG_ITEMS]
        request_delay = config[CONFIG_REQUEST_DELAY]

        item_count = str(len(items_to_check))
        print(ITEM_COUNT_MSG.format(item_count))

        check_stock(input(PROCEED_PROMPT_MSG.format(item_count)))
    except yaml.YAMLError as exception:
        print(exception)