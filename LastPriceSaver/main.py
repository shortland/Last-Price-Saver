import os
import sys
import time
import json
import asyncio
import datetime

import pytz
import tdameritrade
import mysql.connector
import prometheus_client

from LastPriceSaver.config.env import (
    QUOTE_SYMBOLS,
    API_KEY,
    TOKEN_PATH,
    MYSQL_ROOT_PASSWORD,
    PROMETHEUS_PORT
)
from LastPriceSaver.utils.time import current_milli_time
from LastPriceSaver.utils.logger import logger
from LastPriceSaver.utils.secrets_reader import read_refresh_token
from LastPriceSaver.utils.metrics import (
    db_connect_error,
    db_insert_error,
    db_commit_error,
    tda_quotes_error,
    sleeper_inactive,
    active_pulse,
    skipped_sleep,
    skipped_sleep_duration,
    time_slept
)


def main() -> None:
    logger.debug("Attempting to create tda-api client")
    client = tdameritrade.TDClient(
        client_id=API_KEY,
        refresh_token=read_refresh_token(TOKEN_PATH)
    )

    logger.debug("Starting prometheus metrics server")
    prometheus_client.start_http_server(
        int(PROMETHEUS_PORT)
    )

    while True:
        start_time = current_milli_time()
        time_sec = int(time.time())

        # Only record data after 9pm and before 5pm
        # Not exactly 9:30 so we can sleep for a minute at a time...
        # Additionally, if the weekday is 5 (saturday) or 6 (sunday) - sleep.
        now = datetime.datetime.now(pytz.utc)
        if now.hour < 14 or now.hour > 22 or \
            now.weekday() is 6 or now.weekday() is 5:
            
            logger.debug("Not time yet... Sleeping for 60s")
            sleeper_inactive.inc()
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
        actual_sleep = 1.0 - ((current_milli_time() - start_time) / 1000.0)

        if actual_sleep <= 0.0:
            skipped_sleep.inc()
            skipped_sleep_duration.inc(abs(actual_sleep) + 1.0)
            logger.debug(
                "Not sleeping, sleep was too small: '{}'".format(actual_sleep)
            )
            continue

        logger.debug("Sleeping for: '{}'".format(actual_sleep))
        time_slept.inc(actual_sleep)
        time.sleep(actual_sleep)


async def get_and_save_quotes(client: tdameritrade.TDClient, quotes, start_time: float, time_sec: int) -> None:
    """
    Get the quotes and then save them to DB.
    """

    try:
        active_pulse.inc()
        quotes = client.quote(QUOTE_SYMBOLS)

        await write_quotes_to_db(quotes, start_time, time_sec)
    except Exception as error:
        logger.error(
            "Unable to get quote data for symbols: {}".format(error)
        )
        tda_quotes_error.inc()


async def write_quotes_to_db(quotes, time_milli: float, time_sec: int) -> None:
    """
    Eventually either use a queue or refresh login details as necessary...
    It's excessive to login each time.
    """

    logger.debug("Beginning save data to db")

    # TODO: This essentially creates a new DB connection every second... Which is a waste of resources.
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
        db_connect_error.inc()
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
            db_insert_error.inc()

    try:
        db.commit()
    except Exception as error:
        logger.error("Unable to commit changes to db: {}".format(error))
        db_commit_error.inc()


if __name__ == '__main__':
    main()
