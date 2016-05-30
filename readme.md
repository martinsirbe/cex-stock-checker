```
                     _             _           _               _
                    | |           | |         | |             | |
  ___ _____  __  ___| |_ ___   ___| | __   ___| |__   ___  ___| | _____ _ __
 / __/ _ \ \/ / / __| __/ _ \ / __| |/ /  / __| '_ \ / _ \/ __| |/ / _ \ '__|
| (_|  __/>  <  \__ \ || (_) | (__|   <  | (__| | | |  __/ (__|   <  __/ |
 \___\___/_/\_\ |___/\__\___/ \___|_|\_\  \___|_| |_|\___|\___|_|\_\___|_|

```
CEX UK is a shop that sells second-hand items, such as console games, movies, various electronic products, etc.
This is a simple script written in Python that is used to check CEX UK website to see if items are in stock.

CEX UK website - https://uk.webuy.com/

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
- [ ] Check item availability in a specific shop
- [ ] Previous price check to notify when the price drops.
- [ ] Notify about changes via email

[Python]: <https://www.python.org/>
[PyYAML]: <http://pyyaml.org/>
[Requests]: <http://docs.python-requests.org/en/master/>