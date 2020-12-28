auth:
	# Install latest tda-api not available elsewhere...
	git clone https://github.com/alexgolec/tda-api.git
	python3 -m pip install tda-api/

	python3 -m pip install -r Tokener/requirements.txt
	python3 Tokener/main.py

build:
	docker-compose build --no-cache

run:
	docker-compose up -d

# sql:
# 	docker exec -it maria_db bash

clean:
	docker-compose down