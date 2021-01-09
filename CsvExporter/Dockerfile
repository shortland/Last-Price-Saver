FROM python:latest

# Copy over src to the container
WORKDIR /app
COPY CsvExporter/ /app/CsvExporter

# Install dependencies
RUN python -m pip install -r /app/CsvExporter/requirements.txt

# Run app
CMD python CsvExporter/main.py