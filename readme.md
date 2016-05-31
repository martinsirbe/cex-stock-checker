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

CEX UK website - https://uk.webuy.com/

### Configuration
All configuration goes into `config.yaml`
- `items` - An array of item titles that will be used to make a stock check.
- `requestDelay` - Request delay in seconds between HTTP GET requests. By default is set to 2 seconds.
- `storeId` - You can find store ID by making a call to CEX website and making a refined search by selecting a specific store's stock.
Example:
After selecting `London W1 Tottenham Crt Rd` produces the following URL:
https://uk.webuy.com/search/index.php?stext=crystal+castles+III&section=&rad_which_stock=3&refinebystore=1
The store ID is defined after `refinebystore`, in this example it's 1.
By default is not set.
- `proceedPromptDisabled` - If set to `true` will disable the prompt before continuing with stock check. By default set to false.

Executing the following link -
https://uk.webuy.com/search/index.php?stext=crystal+castles+III&section=&rad_which_stock=3&refinebystore=1
You will notice that on the right side `Available at Store - London W1 Tottenham Crt Rd` and  (store ID can be found after refinebystore, e.q. 1)

### How to run it?
1. Clone the project
2. cd into the directory and update the config.yaml file with item IDs that you wish to check.
3. execute following command `python3 cex_stock_checker.py` and follow instructions.

### What is used?
- [Python] version 3.5.1
- [Requests] version 2.10.0
- [PyYAML] version 3.11

### To do list
- [x] Check if items are in stock
- [x] Check item availability in a specific shop
- [ ] Previous price check to notify when the price drops.
- [ ] Notify about changes via email

[Python]: <https://www.python.org/>
[PyYAML]: <http://pyyaml.org/>
[Requests]: <http://docs.python-requests.org/en/master/>