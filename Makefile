.PHONY: requirements
requirements:
	pip3 install -r requirements.txt

.PHONY: run
run:
	python3 stock_check.py

.PHONY: load-stores
load-stores:
	@echo "Updating 'stores.yaml' file..."
	@python3 load_stores.py