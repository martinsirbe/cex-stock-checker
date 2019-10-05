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

.PHONY: docker-run
docker-run:
	docker run -e CUSTOM_CONFIG="/custom_config/$(CUSTOM_CONFIG)" \
	    -v "$$PWD":"/custom_config" martinsirbe/cex-stock-checker:latest

.PHONY: docker-build-local
docker-build-local:
	docker build -f Dockerfile -t cex-stock-checker .

.PHONY: docker-run-local
docker-run-local: docker-build-local
	docker run cex-stock-checker:latest
