auth:
	# Install latest tda-api not available elsewhere...
	git clone https://github.com/alexgolec/tda-api.git
	python3 -m pip install tda-api/

	python3 -m pip install -r Tokener/requirements.txt
	python3 Tokener/main.py

csv:
	docker-compose up csv-exporter

import:
	docker-compose up csv-importer

build:
	docker-compose build --no-cache

run:
	docker-compose up -d lps-db main-box

clean:
	docker-compose down