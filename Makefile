.PHONY: requirements
requirements:
	pip3 install -r requirements.txt

.PHONY: run
run:
	python3 cex_stock_checker.py
