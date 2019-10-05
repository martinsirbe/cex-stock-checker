.PHONY: requirements
requirements:
	pip3 install -r requirements.txt

.PHONY: run
run:
	python3 stock_check.py

.PHONY: load-stores
load-stores:
	@echo "Updating 'config/stores.yaml' file..."
	@python3 load_stores.py

.PHONY: docker-build
docker-build:
	docker build -f Dockerfile -t cex-stock-checker .

.PHONY: docker-run
docker-run: docker-build
	docker run cex-stock-checker:latest
