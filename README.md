# CEX Stock Checker

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmartinsirbe%2Fcex-stock-checker.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmartinsirbe%2Fcex-stock-checker?ref=badge_shield) 
[![CircleCI](https://circleci.com/gh/martinsirbe/cex-stock-checker.svg?style=svg)](https://circleci.com/gh/martinsirbe/cex-stock-checker)  

[CEX UK](CEX) is a second-hand shop where you can buy video games, movies, various electronic products etc. 
The initial goal of this project was to add a cron job which would check the CEX stock and notify me when 
some specific games are available in my local store.  
`stock_check.py` - a simple Python script used to check CEX UK API to verify whether the specified items are in the stock.  
`load_stores.py` - maps CEX store ID to store name and writes mapped values to the `config/stores.yaml` file. By default the `stores.yaml` 
is provided, however you might want to run `make load-stores` if the store you are looking for isn't included.  

Additionally, it's possible to configure this script to send the stock check results to a specified email address. 
Any contributions are welcome!

## Configuration
The configuration file - `config/checker.yaml`:  
- `items` - An array of item titles that will be used to make a stock check.
- `request_delay` - Request delay in seconds between HTTP GET requests. By default is set to 2 seconds.
- `store_ids` - Check `config/stores.yaml` for CEX store IDs, alternatively you can find store ID by making 
a call to CEX website and making a refined search by selecting a specific store's stock.  
Example:  
After selecting `London W1 Tottenham Crt Rd` produces the following URL:  
https://uk.webuy.com/search/index.php?stext=crystal+castles+III&section=&rad_which_stock=3&refinebystore=1  
The store ID is defined after `refinebystore`, in this example it's `1`.  

**The following configuration values aren't set**:
- `proceed_prompt_enabled` - If set to `true` will disable the prompt before continuing with the stock check. By default is set to true.
- `send_email_enabled` - If set to `true` will send a message containing the stock check result to the specified email address. By default is set to false.
- `email` - The message will be sent from this email address.
- `email_pass` - The password for the email address.
- `to_email` - The message will be sent to this email address.
- `smtp_host` - The SMTP server host.
- `smtp_port` - The SMTP port number.

## Run it
### Locally
1. Clone the project
2. Update the `config/checker.yaml` file
3. Install requirements by running `make requirements`
4. Run the script `make run`

### Docker
1. Run `make docker-run-local` to build a docker image locally and to run it.  
2. Alternatively, it's possible to use prebuilt `martinsirbe/cex-stock-checker` docker image by 
running `make docker-run CUSTOM_CONFIG=config/checker.yaml`, where `CUSTOM_CONFIG` points to the custom 
configuration file relative to the root of this project.

## Store IDs to Names mapping
1. To map Store IDs to store names, simply run `make load-stores`. This will create a new `config/stores.yaml` file, 
which will contain the mapping between the CEX store ID and name, e.g. `1: London W1 Tottenham Crt Rd`.

## How to run it on Ubuntu 14.04.4 LTS with CRON?
1. Run `crontab -e` and add following line, where `ubuntu` is your home directory name:
```
30 10 * * * cd /home/ubuntu/path/to/cex-stock-checker/ && python3 stock_check.py
```
The above example would execute the script every day at 10:30.
You can use following CRON generator to run script at your own specified time - http://crontab-generator.org/

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.  
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmartinsirbe%2Fcex-stock-checker.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmartinsirbe%2Fcex-stock-checker?ref=badge_large)

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

[CEX]: https://uk.webuy.com/
