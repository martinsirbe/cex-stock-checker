import yaml
import requests
import smtplib
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CONFIG_YAML = "config.yaml"
MESSAGE_HTML = "message.html"

EMAIL_TO_FIELD = "To"
EMAIL_FROM_FIELD = "From"
EMAIL_SUBJECT_FIELD = "Subject"
EMAIL_SUBJECT = "CEX stock check results for {} item's."
EMAIL_MESSAGE_TYPE = "html"
EMAIL_MESSAGE_SENT = "An email has been sent to {}"

HTML_ITEM_IN_STOCK_TAG_PATTERN = "\">{}</a></h1>"
HTML_NO_ITEMS = "<i>--- no items ---</i><br>"
HTML_LIST_ELEMENT = "<li>{}</li>"

INPUT_YES = "y"
INPUT_NO = "n"

CONFIG_REQUEST_DELAY = "request_delay"
CONFIG_ITEMS = "items"
CONFIG_STORE_ID = "store_id"
CONFIG_PROMPT_ENABLED = "proceed_prompt_enabled"
CONFIG_SEND_EMAIL_ENABLED = "send_email_enabled"
CONFIG_EMAIL = "email"
CONFIG_EMAIL_PASS = "email_pass"
CONFIG_TO_EMAIL = "to_email"
CONFIG_SMTP_PORT = "smtp_port"
CONFIG_SMTP_HOST = "smtp_host"

ANY_STORE_URL = "https://uk.webuy.com/search/index.php?stext={}&section=&is=1"
SPECIFIC_STORE_URL = "https://uk.webuy.com/search/index.php?stext={}&section=&rad_which_stock=3&refinebystore={}&is=1"

CHECK_URL = "https://uk.webuy.com/product.php?sku={}#."
PROCEED_PROMPT_MSG = "Do you wish to continue to check the stock for {} items? (y/n)"
OUT_OF_STOCK_SPECIFIC_SHOP_MSG = "-  {} is currently out of stock (Store ID - {})."
IN_STOCK_SPECIFIC_SHOP_MSG = "+  {} is in stock (Store ID - {})."
OUT_OF_STOCK_MSG = "-  {} is currently out of stock."
IN_STOCK_MSG = "+  {} is in stock."
ABORT_MSG = "Aborting the stock check."
WRONG_INPUT_MSG = "Sorry, I didn't get that, please choose either y or n"
ITEM_COUNT_MSG = "Currently there are {} items in your check list."


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

        if HTML_ITEM_IN_STOCK_TAG_PATTERN.format(item_title) in response.text:
            if store_ids is not None:
                in_stock.append(item_title + " (Store ID - " + str(store_id) + ")")
                print(IN_STOCK_SPECIFIC_SHOP_MSG.format(item_title, str(store_id)))
            else:
                in_stock.append(item_title)
                print(IN_STOCK_MSG.format(item_title))
        else:
            if store_ids is not None:
                out_of_stock.append(item_title + " (Store ID - " + str(store_id) + ")")
                print(OUT_OF_STOCK_SPECIFIC_SHOP_MSG.format(item_title, str(store_id)))
            else:
                out_of_stock.append(item_title)
                print(OUT_OF_STOCK_MSG.format(item_title))


def send_email(in_stock, out_of_stock):
    formatted_in_stock_items, formatted_out_of_stock_items, checklist_items = format_checked_items(in_stock, out_of_stock)

    msg = MIMEMultipart("alternative")
    msg[EMAIL_SUBJECT_FIELD] = str.format(EMAIL_SUBJECT, item_count)
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
        response = requests.get(ANY_STORE_URL.format(item_title))
    else:  # Will check specific store stock for given item.
        response = requests.get(SPECIFIC_STORE_URL.format(item_title, store_id))
    return response


with open(CONFIG_YAML, "r", -1, "utf-8") as stream:
    try:
        config = yaml.load(stream)
        items_to_check = config[CONFIG_ITEMS]
        request_delay = config[CONFIG_REQUEST_DELAY]
        store_ids = config[CONFIG_STORE_ID]
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
