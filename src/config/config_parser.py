import configparser
import os
from dataclasses import dataclass
from urllib import parse

import urllib3

config = configparser.ConfigParser()
config.read("config.ini")
base_dir = os.path.abspath('.')

os.environ["NLS_LANG"] = "AMERICAN_AMERICA.AL32UTF8"
urllib3.disable_warnings()


@dataclass(init=False)
class SqLite:
    uri = f'sqlite:///{base_dir}/media/database/development.db'


@dataclass(init=False)
class ApplicationDatabase:
    """Class for database handling"""
    # If another database required create its class and change the uri as needed
    uri = SqLite.uri if config['DATABASE']['DATABASE'] == 'SQLITE' else ''
    table_prefix = config['DATABASE']['TABLE_PREFIX']


@dataclass(init=False)
class Application:
    SECRET_KEY = config["APPLICATION"]["SECRET_KEY"]
    WTF_CSRF_SECRET_KEY = parse.quote_plus(config['APPLICATION']['WTF_CSRF_SECRET_KEY'])
    SECURITY_USER_IDENTITY_ATTRIBUTES = 'username'
    FLASK_ADMIN_SWATCH = "lumen"
    SQLALCHEMY_ECHO = config["APPLICATION"]["SQLALCHEMY_ECHO"] == "true"
    SQLALCHEMY_TRACK_MODIFICATIONS = config["APPLICATION"]["SQLALCHEMY_TRACK_MODIFICATIONS"] == "true"
    SQLALCHEMY_DATABASE_URI = ApplicationDatabase.uri

    @staticmethod
    def init_app(app):
        pass


@dataclass()
class Media:
    media_path = config["FILES"]["MEDIA_PATH"]
    log_file_info = config["LOGGER"]["LOG_FILE_INFO"]
    log_file_error = config["LOGGER"]["LOG_FILE_ERROR"]

    def __init__(self):
        os.makedirs(self.media_path, exist_ok=True)
        os.makedirs(os.path.join(self.media_path, 'database'), exist_ok=True)


@dataclass(init=False)
class AcunetixApi:
    api_key = parse.quote_plus(config['ACUNETIX']['API_KEY'])
    api_url = config['ACUNETIX']['API_URL']


@dataclass(init=True)
class AdminUser:
    email = config['ADMIN_USER']['EMAIL']
    username = config['ADMIN_USER']['USERNAME']
    password = config['ADMIN_USER']['PASSWORD']
    is_admin = True
