import os
from dotenv import load_dotenv

load_dotenv()

CEMIG_USERNAME = os.getenv('CEMIG_USERNAME')
CEMIG_PASSWORD = os.getenv('CEMIG_PASSWORD')

APIKEY_2CAPTCHA = os.getenv('APIKEY_2CAPTCHA')