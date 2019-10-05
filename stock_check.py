import yaml
import requests
import smtplib
import os.path
import sys
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CONFIG_YAML = "config/checker.yaml"
STORES_YAML = "config/stores.yaml"
MESSAGE_HTML = "templates/message.html"

EMAIL_TO_FIELD = "To"
EMAIL_FROM_FIELD = "From"
EMAIL_SUBJECT_FIELD = "Subject"
EMAIL_SUBJECT = "CEX stock check results. {} item's in stock."
EMAIL_MESSAGE_TYPE = "html"
EMAIL_MESSAGE_SENT = "An email has been sent to {}"

HTML_ITEM_IN_STOCK_TAG_PATTERN = "\">{}</a></h1>"
HTML_NO_ITEMS = "<i>--- no items ---</i><br>"
HTML_LIST_ELEMENT = "<li>{}</li>"

INPUT_YES = "y"
INPUT_NO = "n"

CONFIG_REQUEST_DELAY = "request_delay"
CONFIG_ITEMS = "items"
CONFIG_STORE_IDS = "store_ids"
CONFIG_PROMPT_ENABLED = "proceed_prompt_enabled"
CONFIG_SEND_EMAIL_ENABLED = "send_email_enabled"
CONFIG_EMAIL = "email"
CONFIG_EMAIL_PASS = "email_pass"
CONFIG_TO_EMAIL = "to_email"
CONFIG_SMTP_PORT = "smtp_port"
CONFIG_SMTP_HOST = "smtp_host"

CEX_API_URL = "https://wss2.cex.uk.webuy.io/v3"
ANY_STORE_SEARCH = "{}/boxes?q={}"
SPECIFIC_STORE_SEARCH = "{}/boxes?q={}&storeIds=[{}]"
DEFAULT_QUERY_PARAMS = "&firstRecord=1&count=50&sortBy=relevance&sortOrder=desc"

PROCEED_PROMPT_MSG = "Do you wish to continue to check the stock for {} items? (y/n)"
OUT_OF_STOCK_SPECIFIC_SHOP_MSG = "-  {} is currently out of stock (Store - {})."
IN_STOCK_SPECIFIC_SHOP_MSG = "+  {} is in stock (Store - {})."
OUT_OF_STOCK_MSG = "-  {} is currently out of stock."
IN_STOCK_MSG = "+  {} is in stock."
ABORT_MSG = "Aborting the stock check."
WRONG_INPUT_MSG = "Sorry, I didn't get that, please choose either y or n"
ITEM_COUNT_MSG = "Currently there are {} items in your check list."
STORES_YAML_FILE_NOT_PRESENT_MSG = 'Stores YAML file not created. Will output store IDs instead of store names.'
NO_CONFIG_FILE_PRESENT_ERROR = 'No config/checker.yaml file present.'
STORE_NAME_NOT_FOUND = 'No name for store ID - {}'


def check_stock(proceed):
    if proceed == INPUT_YES:

        in_stock = []
        out_of_stock = []

        if store_ids is not None:
            for store_id in store_ids:
                check(in_stock, out_of_stock, store_id)
        else:
            check(in_stock, out_of_stock, None)

        if send_email_enabled:
            send_email(in_stock, out_of_stock)
    elif proceed == INPUT_NO:
        print(ABORT_MSG)
    else:
        print(WRONG_INPUT_MSG)
        check_stock(input(PROCEED_PROMPT_MSG.format(item_count)))


def check(in_stock, out_of_stock, store_id):
    for item in items_to_check:
        sleep(float(request_delay))
        item_title = str(item)

        response = get_request(item_title, store_id)

        if response.json().get("response").get("data") is not None:
            report_item_availability(IN_STOCK_MSG, IN_STOCK_SPECIFIC_SHOP_MSG, in_stock, item_title, store_id)
        else:
            report_item_availability(OUT_OF_STOCK_MSG, OUT_OF_STOCK_SPECIFIC_SHOP_MSG, out_of_stock, item_title, store_id)


def report_item_availability(all_shop_message, specific_shop_message, stock, item_title, store_id):
    if store_ids is not None:
        store = get_store_name_from_id(store_id)
        stock.append(item_title + " (" + str(store) + ")")
        print(specific_shop_message.format(item_title, str(store)))
    else:
        stock.append(item_title)
        print(all_shop_message.format(item_title))


def get_store_name_from_id(store_id):
    store = str(store_id)
    if os.path.isfile(STORES_YAML):
        try:
            store_name = stores[store]
            if store_name is not None:
                store = store_name
        except Exception:
            print(STORE_NAME_NOT_FOUND.format(store_id))
    return store


def send_email(in_stock, out_of_stock):
    formatted_in_stock_items, formatted_out_of_stock_items, checklist_items = format_checked_items(in_stock, out_of_stock)

    msg = MIMEMultipart("alternative")
    msg[EMAIL_SUBJECT_FIELD] = str.format(EMAIL_SUBJECT.format(len(in_stock)), item_count)
    msg[EMAIL_FROM_FIELD] = email
    msg[EMAIL_TO_FIELD] = to_email

    with open(MESSAGE_HTML, "r") as email_html_file:
        html_template = email_html_file.read()

    html = MIMEText(
        str.format(
            html_template,
            formatted_in_stock_items,
            formatted_out_of_stock_items,
            checklist_items
        ),
        EMAIL_MESSAGE_TYPE
    )
    msg.attach(html)

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, email_pass)
    server.sendmail(email, to_email, msg.as_string())
    server.close()
    print(str.format(EMAIL_MESSAGE_SENT, to_email))


def format_checked_items(in_stock, out_of_stock):
    formated_in_stock_items = ""
    formated_out_of_stock_items = ""
    checklist_items = ""

    if not in_stock:
        formated_in_stock_items = HTML_NO_ITEMS
    else:
        for item in in_stock:
            formated_in_stock_items += str.format(HTML_LIST_ELEMENT, item)
    if not out_of_stock:
        formated_out_of_stock_items = HTML_NO_ITEMS
    else:
        for item in out_of_stock:
            formated_out_of_stock_items += str.format(HTML_LIST_ELEMENT, item)

    if not items_to_check:
        checklist_items = HTML_NO_ITEMS
    else:
        for item in items_to_check:
            checklist_items += str.format(HTML_LIST_ELEMENT, item)
    return formated_in_stock_items, formated_out_of_stock_items, checklist_items


# Make a get request to Cex with given item title.
def get_request(item_title, store_id):
    if store_ids is None:  # By default store_id is set to None, therefore will check all stores.
        response = requests.get(ANY_STORE_SEARCH.format(CEX_API_URL, item_title, DEFAULT_QUERY_PARAMS))
    else:  # Will check specific store stock for given item.
        response = requests.get(SPECIFIC_STORE_SEARCH.format(CEX_API_URL, item_title, store_id, DEFAULT_QUERY_PARAMS))
    return response

try:
    with open(STORES_YAML, "r", -1, "utf-8") as stream:
        try:
            stores = yaml.load(stream, Loader=yaml.BaseLoader)
        except yaml.YAMLError as exception:
            print(exception)
except FileNotFoundError:
    print(STORES_YAML_FILE_NOT_PRESENT_MSG)

try:
    with open(CONFIG_YAML, "r", -1, "utf-8") as stream:
        try:
            config = yaml.load(stream, Loader=yaml.FullLoader)
            items_to_check = config[CONFIG_ITEMS]
            request_delay = config[CONFIG_REQUEST_DELAY]
            store_ids = config[CONFIG_STORE_IDS]
            prompt_enabled = config[CONFIG_PROMPT_ENABLED]
            send_email_enabled = config[CONFIG_SEND_EMAIL_ENABLED]
            email = config[CONFIG_EMAIL]
            email_pass = config[CONFIG_EMAIL_PASS]
            to_email = config[CONFIG_TO_EMAIL]
            smtp_host = config[CONFIG_SMTP_HOST]
            smtp_port = config[CONFIG_SMTP_PORT]

            item_count = str(len(items_to_check))
            print(ITEM_COUNT_MSG.format(item_count))

            if prompt_enabled:
                check_stock(input(PROCEED_PROMPT_MSG.format(item_count)))
            else:
                check_stock(INPUT_YES)

        except yaml.YAMLError as exception:
            print(exception)
except FileNotFoundError:
    sys.exit(NO_CONFIG_FILE_PRESENT_ERROR)
