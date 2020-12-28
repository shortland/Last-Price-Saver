import os
import sys
import time
import json
import asyncio
import datetime

import tdameritrade
import mysql.connector
import prometheus_client

from LastPriceSaver.config.env import (
    QUOTE_SYMBOLS,
    DATA_PATH,
    API_KEY,
    TOKEN_PATH,
    MYSQL_ROOT_PASSWORD,
    PROMETHEUS_PORT
)
from LastPriceSaver.utils.time import current_milli_time
from LastPriceSaver.utils.logger import logger
from LastPriceSaver.utils.secrets_reader import read_refresh_token


def main() -> None:
    logger.debug("Attempting to create tda-api client")
    client = tdameritrade.TDClient(
        client_id=API_KEY,
        refresh_token=read_refresh_token(TOKEN_PATH)
    )

    logger.debug("Starting prometheus metrics server")
    prometheus_client.start_http_server(PROMETHEUS_PORT)

    while True:
        start_time = current_milli_time()
        time_sec = int(time.time())

        # Only record data after 9pm and before 5pm
        # Not exactly 9:30 so we can sleep for a minute at a time...
        now = datetime.datetime.now()
        if now.hour < 14 or now.hour > 22:
            logger.debug("Not time yet... Sleeping for 60s")
            time.sleep(60)
            continue

        logger.debug("Getting quotes data")
        asyncio.run(
            get_and_save_quotes(
                client,
                QUOTE_SYMBOLS,
                start_time,
                time_sec
            )
        )

        """ Sleeping Calculations """
        actual_sleep = 1.0 - ((current_milli_time() - start_time) / 1000)

        if actual_sleep <= 0.0:
            logger.debug(
                "Not sleeping, sleep was too small: '{}'".format(actual_sleep)
            )
            continue

        logger.debug("Sleeping for: '{}'".format(actual_sleep))
        time.sleep(actual_sleep)


async def get_and_save_quotes(client: tdameritrade.TDClient, quotes, start_time: float, time_sec: int) -> None:
    """
    Get the quotes and then save them to DB.
    """

    try:
        quotes = client.quote(QUOTE_SYMBOLS)

        await write_quotes_to_db(quotes, start_time, time_sec)
    except Exception as error:
        logger.error(
            "Unable to get quote data for symbols: {}".format(error)
        )


async def write_quotes_to_db(quotes, time_milli: float, time_sec: int) -> None:
    """
    Eventually either use a queue or refresh login details as necessary...
    It's excessive to login each time.
    """

    logger.debug("Beginning save data to db")

    try:
        db = mysql.connector.connect(
            host='lps-host',
            user='root',
            passwd=MYSQL_ROOT_PASSWORD,
            database='last_price_saver'
        )
        cursor = db.cursor()
    except Exception as error:
        logger.error("Unable to create connection to db: {}".format(error))
        return

    for quote in quotes:
        try:
            insert_query = """
                INSERT INTO last_price
                    (timestamped, timestamp_milli, symbol, price, json)
                VALUES
                    ({0}, {1}, '{2}', {3}, '{4}')
            """.format(
                time_sec,
                time_milli,
                quote,
                quotes.get(quote).get('lastPrice'),
                "test"
            )
            cursor.execute(insert_query)
        except Exception as error:
            logger.error("Unable to insert into db: {}; {}".format(
                error, insert_query
            ))

    try:
        db.commit()
    except Exception as error:
        logger.error("Unable to commit changes to db: {}".format(error))


if __name__ == '__main__':
    main()
