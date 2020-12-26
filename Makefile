auth:
	echo some authentication steps here

build:
	docker-compose build --no-cache

run:
	docker-compose up

clean:
	docker-compose down