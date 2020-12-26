import datetime

from loguru import logger

from HistoricalQuoteData.config.env import (
    LOG_PATH,
    LOG_LEVEL
)

logger.add(
    "{}/{}.log".format(
        LOG_PATH,
        datetime.date.today()
    ),
    format="{time} {level} {message}",
    enqueue=True,
    level=LOG_LEVEL
)
