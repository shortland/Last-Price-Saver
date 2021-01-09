FROM python:latest

# Copy over src to the container
WORKDIR /app
COPY AlgoMerger/ /app/AlgoMerger

# Install dependencies
RUN python -m pip install -r /app/AlgoMerger/requirements.txt

# Run app
CMD python AlgoMerger/main.py