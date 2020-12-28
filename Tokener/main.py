import os
import pathlib

import tda
import dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

env_path = pathlib.Path('.') / '.env'
dotenv.load_dotenv(dotenv_path=env_path)

tda.auth.client_from_login_flow(
    webdriver=webdriver.Chrome(ChromeDriverManager().install()),
    api_key=os.getenv('API_KEY'),
    redirect_url=os.getenv('REDIRECT_URI'),
    token_path="{0}/{1}".format(
        os.getenv('EXTERNAL_TOKEN_PATH'),
        os.getenv('TOKEN_FILE_NAME')
    )
)
