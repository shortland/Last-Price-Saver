import os
import sys
import json
import requests
import urllib.parse

import tda
from authlib.oauth2.rfc6749 import OAuth2Token

from LastPriceSaver.config.env import (
    API_KEY,
    REDIRECT_URI,
    TOKEN_PATH,
    AUTH_CODE
)
from LastPriceSaver.utils.logger import logger


def setup() -> tda.client.Client:
    logger.debug("Token path: {}".format(TOKEN_PATH))

    if os.path.exists(TOKEN_PATH):
        logger.debug("Use existing token from file")

        return tda.auth.client_from_token_file(
            TOKEN_PATH,
            API_KEY
        )
    elif AUTH_CODE == '':
        logger.debug("First need to get authorization code.")

        logger.info(
            "Login to TDAmeritrade with the below link:\n"
            "https://auth.tdameritrade.com/auth?" + urllib.parse.urlencode({
                'response_type': 'code',
                'redirect_uri': REDIRECT_URI,
                'client_id': API_KEY + '@AMER.OAUTHAP'
            })
        )

        return None
    else:
        logger.debug("Using specified auth-code to get tokens")

        tokens = requests.post(
            "https://api.tdameritrade.com/v1/oauth2/token",
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'grant_type': 'authorization_code',
                'refresh_token': '',
                'access_type': 'offline',
                'code': urllib.parse.unquote(AUTH_CODE),
                'client_id': API_KEY,
                'redirect_uri': REDIRECT_URI
            }
        )

        if tokens.status_code != 200:
            logger.error(
                "Possible invalid Auth-Code. Delete the existing one and retrieve a new one."
            )

            return None

        oauth2_token = OAuth2Token(json.loads(tokens.text))

        with open(TOKEN_PATH, 'w') as f:
            json.dump(oauth2_token, f)

        return tda.auth.client_from_token_file(
            TOKEN_PATH,
            API_KEY
        )
