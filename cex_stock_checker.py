import yaml
import requests
from time import sleep

PROMPT_DISABLED = "proceedPromptDisabled"

ITEM_IN_STOCK_TAG_PATTERN = "\">{}</a></h1>"

INPUT_YES = "y"
INPUT_NO = "n"

CONFIG_YAML = "config.yaml"
CONFIG_REQUEST_DELAY = "requestDelay"
CONFIG_ITEMS = "items"
CONFIG_STORE_ID = "storeId"

ANY_STORE_URL = "https://uk.webuy.com/search/index.php?stext={}&section=&is=1"
SPECIFIC_STORE_URL = "https://uk.webuy.com/search/index.php?stext={}&section=&rad_which_stock=3&refinebystore={}&is=1"

CHECK_URL = "https://uk.webuy.com/product.php?sku={}#."
PROCEED_PROMPT_MSG = "Do you wish to continue to check the stock for {} items? (y/n)"
OUT_OF_STOCK_MSG = "-  {} is currently out of stock."
IN_STOCK_MSG = "+  {} is in stock."
ABORT_MSG = "Aborting the stock check."
WRONG_INPUT_MSG = "Sorry, I didn't get that, please choose either y or n"
ITEM_COUNT_MSG = "Currently there are {} items in your check list."


def check_stock(proceed):
    if proceed == INPUT_YES:
        for item in items_to_check:
            sleep(float(request_delay))
            item_title = str(item)

            response = get_request(item_title)

            if ITEM_IN_STOCK_TAG_PATTERN.format(item_title) in response.text:
                print(IN_STOCK_MSG.format(item_title))
            else:
                print(OUT_OF_STOCK_MSG.format(item_title))

    elif proceed == INPUT_NO:
        print(ABORT_MSG)
    else:
        print(WRONG_INPUT_MSG)
        check_stock(input(PROCEED_PROMPT_MSG.format(item_count)))


# Make a get request to Cex with given item title.
def get_request(item_title):
    if store_id is None:  # By default store_id is set to None, therefore will check all stores.
        response = requests.get(ANY_STORE_URL.format(item_title))
    else:  # Will check specific store stock for given item.
        response = requests.get(SPECIFIC_STORE_URL.format(item_title, store_id))
    return response


with open(CONFIG_YAML, "r") as stream:
    try:
        config = yaml.load(stream)
        items_to_check = config[CONFIG_ITEMS]
        request_delay = config[CONFIG_REQUEST_DELAY]
        store_id = config[CONFIG_STORE_ID]
        promptDisabled = config[PROMPT_DISABLED]

        item_count = str(len(items_to_check))
        print(ITEM_COUNT_MSG.format(item_count))

        if promptDisabled:
            check_stock(INPUT_YES)
        else:
            check_stock(input(PROCEED_PROMPT_MSG.format(item_count)))

    except yaml.YAMLError as exception:
        print(exception)
