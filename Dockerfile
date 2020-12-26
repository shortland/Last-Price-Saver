FROM ubuntu:20.04

# Basic setups and upgrades for python3
RUN apt-get update && \
    apt-get upgrade -y && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y \
    software-properties-common \
    python3.8 \
    python3-pip \
    git
RUN cp /usr/bin/python3 /usr/bin/python

# Copy over src to the container
WORKDIR /app
COPY HistoricalQuoteData/ /app/HistoricalQuoteData

# Install latest tda-api version; not tagged nor released currently 
# Eventually once they move onto the next tag after 0.7.1, can install from requirements.txt
RUN git clone https://github.com/alexgolec/tda-api.git
RUN python -m pip install tda-api/

# Install dependencies
COPY requirements.txt /app/
RUN python -m pip install -r requirements.txt

# Run app
CMD python -m HistoricalQuoteData