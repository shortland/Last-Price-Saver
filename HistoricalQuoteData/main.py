import os
import sys
import json
import pathlib
import requests
import urllib.parse

import tda

from HistoricalQuoteData.config.env import (
    QUOTE_SYMBOL,
    DATA_PATH
)
from HistoricalQuoteData.utils.logger import logger
from HistoricalQuoteData.login import login


def main() -> None:
    logger.debug("Attempting to create tda-api client")
    client = login.setup()

    if client is None:
        sys.exit(-1)

    r = client.get_price_history(
        QUOTE_SYMBOL,
        period_type=tda.client.Client.PriceHistory.PeriodType.DAY,
        period=tda.client.Client.PriceHistory.Period.ONE_YEAR,
        frequency_type=tda.client.Client.PriceHistory.FrequencyType.MINUTE,
        frequency=tda.client.Client.PriceHistory.Frequency.EVERY_MINUTE
    )

    assert r.status_code == 200, r.raise_for_status()

    out_dir = "{}/MINUTE_DATA".format(DATA_PATH)
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)

    out_file = "{}/{}.json".format(out_dir, QUOTE_SYMBOL)
    with open(out_file, 'w') as f:
        json.dump(r.json(), f)


if __name__ == '__main__':
    main()
