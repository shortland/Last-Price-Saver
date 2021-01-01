auth:
	# Install latest tda-api not available elsewhere...
	git clone https://github.com/alexgolec/tda-api.git
	python3 -m pip install tda-api/

	python3 -m pip install -r Tokener/requirements.txt
	python3 Tokener/main.py

csv:
	python3 -m pip install -r CsvExporter/requirements.txt
	python3 CsvExporter/main.py

build:
	docker-compose build --no-cache

run:
	docker-compose up -d

clean:
	docker-compose down