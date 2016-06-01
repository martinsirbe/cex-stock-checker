import yaml
import requests
import smtplib
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ITEM_IN_STOCK_TAG_PATTERN = "\">{}</a></h1>"

INPUT_YES = "y"
INPUT_NO = "n"

CONFIG_YAML = "config.yaml"
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
OUT_OF_STOCK_MSG = "-  {} is currently out of stock."
IN_STOCK_MSG = "+  {} is in stock."
ABORT_MSG = "Aborting the stock check."
WRONG_INPUT_MSG = "Sorry, I didn't get that, please choose either y or n"
ITEM_COUNT_MSG = "Currently there are {} items in your check list."


def check_stock(proceed):
    if proceed == INPUT_YES:

        in_stock = []
        out_of_stock = []

        for item in items_to_check:
            sleep(float(request_delay))
            item_title = str(item)

            response = get_request(item_title)

            if ITEM_IN_STOCK_TAG_PATTERN.format(item_title) in response.text:
                in_stock.append(item_title)
                print(IN_STOCK_MSG.format(item_title))
            else:
                out_of_stock.append(item_title)
                print(OUT_OF_STOCK_MSG.format(item_title))

        if send_email_enabled:
            send_email(in_stock, out_of_stock)
    elif proceed == INPUT_NO:
        print(ABORT_MSG)
    else:
        print(WRONG_INPUT_MSG)
        check_stock(input(PROCEED_PROMPT_MSG.format(item_count)))


def send_email(in_stock, out_of_stock):
    formatted_in_stock_items, formatted_out_of_stock_items, checklist_items = format_checked_items(in_stock, out_of_stock)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "CEX stock check results for " + item_count + " item's."
    msg["From"] = email
    msg["To"] = to_email

    with open("email.html", "r") as email_html_file:
        html_template = email_html_file.read()

    html = MIMEText(
        str.format(
            html_template,
            formatted_in_stock_items,
            formatted_out_of_stock_items,
            checklist_items
        ),
        "html"
    )
    msg.attach(html)

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, email_pass)
    server.sendmail(email, to_email, msg.as_string())
    server.close()
    print("An email has been sent to " + to_email)


def format_checked_items(in_stock, out_of_stock):
    formated_in_stock_items = ""
    formated_out_of_stock_items = ""
    checklist_items = ""

    if not in_stock:
        formated_in_stock_items = "<i>--- no items ---</i><br>"
    else:
        for item in in_stock:
            formated_in_stock_items += "<li>" + item + "</li>"
    if not out_of_stock:
        formated_out_of_stock_items = "<i>--- no items ---</i><br>"
    else:
        for item in out_of_stock:
            formated_out_of_stock_items += "<li>" + item + "</li>"

    if not items_to_check:
        checklist_items = "<i>--- no items ---</i><br>"
    else:
        for item in items_to_check:
            checklist_items += "<li>" + item + "</li>"
    return formated_in_stock_items, formated_out_of_stock_items, checklist_items


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
