auth:
	echo some authentication steps here

build:
	docker-compose build --no-cache

run:
	docker-compose up -d

# sql:
# 	docker exec -it maria_db bash

clean:
	docker-compose down