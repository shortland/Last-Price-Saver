build:
	docker build \
		--no-cache \
		-t historical_quote_data .

run:
	docker run -i \
		-v logs:/app/logs \
		-v data:/app/data \
		-v HistoricalQuoteData:/app/HistoricalQuoteData \
		-t historical_quote_data

run_detatched:
	docker run -d \
		-v logs:/app/logs \
		-v data:/app/data \
		-v HistoricalQuoteData:/app/HistoricalQuoteData \
		-t historical_quote_data