import os
import sys
import json
import pathlib
import calendar
import datetime
import requests
import urllib.parse

import tda

from LastPriceSaver.config.env import (
    QUOTE_SYMBOLS,
    DATA_PATH
)
from LastPriceSaver.utils.logger import logger
from LastPriceSaver.login import login


def main() -> None:
    logger.debug("Attempting to create tda-api client")
    client = login.setup()

    if client is None:
        sys.exit(-1)

    for quote_symbol in QUOTE_SYMBOLS:
        logger.debug("Start getting data for symbol: {}".format(quote_symbol))
        year = 2020
        # Temporary, won't work if current month is '1' (january)
        for month in range(datetime.datetime.now().month - 1, datetime.datetime.now().month + 1, 1):
            logger.debug("Start getting data for month: {}".format(month))
            r = client.get_price_history(
                quote_symbol,
                period_type=tda.client.Client.PriceHistory.PeriodType.DAY,
                frequency_type=tda.client.Client.PriceHistory.FrequencyType.MINUTE,
                frequency=tda.client.Client.PriceHistory.Frequency.EVERY_MINUTE,
                start_datetime=datetime.datetime(year, month, 1, 9, 30, 0),
                end_datetime=datetime.datetime(
                    year, month, calendar.monthrange(year, month)[1], 16, 0, 0
                )
            )

            assert r.status_code == 200, r.raise_for_status()

            out_dir = "{}/MINUTE_DATA/{}/{}".format(
                DATA_PATH,
                year,
                datetime.date(year, month, 1).strftime('%B')
            )
            pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)

            out_file = "{}/{}.json".format(out_dir, quote_symbol)
            with open(out_file, 'w') as f:
                json.dump(r.json(), f)


if __name__ == '__main__':
    main()
