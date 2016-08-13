```
                     _             _           _               _
                    | |           | |         | |             | |
  ___ _____  __  ___| |_ ___   ___| | __   ___| |__   ___  ___| | _____ _ __
 / __/ _ \ \/ / / __| __/ _ \ / __| |/ /  / __| '_ \ / _ \/ __| |/ / _ \ '__|
| (_|  __/>  <  \__ \ || (_) | (__|   <  | (__| | | |  __/ (__|   <  __/ |
 \___\___/_/\_\ |___/\__\___/ \___|_|\_\  \___|_| |_|\___|\___|_|\_\___|_|

```
CEX UK is a shop that sells second-hand items, such as console games, movies, various electronic products, etc.
This is a simple script written in Python that is used to check CEX UK website to see if given items are in a specific store stock.
Additionally, it's possible to configure this script to send the stock check result to a specified email address.

CEX UK website - https://uk.webuy.com/

### Configuration
All configuration goes into `config.yaml`
- `items` - An array of item titles that will be used to make a stock check.
- `request_delay` - Request delay in seconds between HTTP GET requests. By default is set to 2 seconds.
- `store_id` - You can find store ID by making a call to CEX website and making a refined search by selecting a specific store's stock.
Example:
After selecting `London W1 Tottenham Crt Rd` produces the following URL:
https://uk.webuy.com/search/index.php?stext=crystal+castles+III&section=&rad_which_stock=3&refinebystore=1
The store ID is defined after `refinebystore`, in this example it's 1.
By default is not set.
- `proceed_prompt_enabled` - If set to `true` will disable the prompt before continuing with the stock check. By default is set to true.
- `send_email_enabled` - If set to `true` will send a message containing the stock check result to the specified email address. By default is set to false.
- `email` - The message will be sent from this email address.
- `email_pass` - The password for the email address.
- `to_email` - The message will be sent to this email address.
- `smtp_host` - The SMTP server host.
- `smtp_port` - The SMTP port number.

### How to run it locally?
1. Clone the project
2. Update the `config.yaml` file
3. Install [PyYAML]:
 * `wget -P /path/to/dir http://pyyaml.org/download/pyyaml/PyYAML-3.11.tar.gz`
 * `tar -xzf PyYAML-3.11.tar.gz`
 * `cd PyYAML-3.11`
 * `python setup.py install`
4. Install [Requests]:
 * `pip install requests`
3. Execute the script `python3 cex_stock_checker.py`

### How to run it on Ubuntu 14.04.4 LTS with CRON?
1. Clone, install required libraries and update the config.yaml file.
2. Add `import os` line at the top in `cex_stock_checker.py`
3. Update `CONFIG_YAML` and `MESSAGE_HTML` values in `cex_stock_checker.py` to use `os.getcwd()` with path to the script location.
Example for user `ubuntu`, full path to script would be `/home/ubuntu/apps/cex-stock-checker/cex_stock_checker.py`

For user `ubuntu` the `cex_stock_checker.py` file changes would be as follow:
```
CONFIG_YAML = os.getcwd() + "/apps/cex-stock-checker/config.yaml"
MESSAGE_HTML = os.getcwd() + "/apps/cex-stock-checker/message.html"
```
4. Run `crontab -e` and add following line, where `ubuntu` is your home directory name:
```
30 10 * * * python3 /home/ubuntu/apps/cex-stock-checker/cex_stock_checker.py >/dev/null 2>&1
```
The above example would execute the script every day at 10:30.
You can use following CRON generator to run script at your own specified time - http://crontab-generator.org/

### What is used?
- [Python] version 3.5.1
- [Requests] version 2.10.0
- [PyYAML] version 3.11

[Python]: <https://www.python.org/>
[PyYAML]: <http://pyyaml.org/>
[Requests]: <http://docs.python-requests.org/en/master/>