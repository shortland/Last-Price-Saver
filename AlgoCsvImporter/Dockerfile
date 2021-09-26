FROM python:latest

# Copy over src to the container
WORKDIR /app
COPY AlgoCsvImporter/ /app/AlgoCsvImporter

# Install dependencies
RUN python -m pip install -r /app/AlgoCsvImporter/requirements.txt

# Run app
CMD python AlgoCsvImporter/main.py