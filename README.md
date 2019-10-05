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

## Configuration
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

## Run it
1. Clone the project
2. Update the `config.yaml` file
3. Install requirements by running `make requirements`
4. Run the script `make run`

## Store IDs to Names mapping
1. To map Store IDs to store names, simply run this command. This will create a new YAML file called stores, which will contain the mapping between the CEX store ID and the store name.
 * `./store_id_to_name_mapper.py`

## How to run it on Ubuntu 14.04.4 LTS with CRON?
1. Run `crontab -e` and add following line, where `ubuntu` is your home directory name:
```
30 10 * * * cd /home/ubuntu/path/to/cex-stock-checker/ && python3 cex_stock_checker.py
```
The above example would execute the script every day at 10:30.
You can use following CRON generator to run script at your own specified time - http://crontab-generator.org/

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.  

## Contributing
* Fork the repository github.com/martinsirbe/cex-stock-checker
* Create your feature branch:
```bash
git checkout -b my-feature-branch
```
* Commit your changes:
```bash
git commit -m 'Add ...'
```
* Push to the branch.
```bash
git push origin my-feature-branch
```
* Create a new pull request and select the `cex-stock-checker` master branch as the base.

## What is used?
- [Python] version 3.5.1
- [Requests] version 2.10.0
- [PyYAML] version 3.11

[Python]: <https://www.python.org/>
[PyYAML]: <http://pyyaml.org/>
[Requests]: <http://docs.python-requests.org/en/master/>