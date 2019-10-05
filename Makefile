.PHONY: requirements
requirements:
	pip3 install -r requirements.txt

.PHONY: run
run:
	./cex_stock_checker.py
