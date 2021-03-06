from flask_restful import Api
from flask_api import FlaskAPI

from app.main.controllers import AppInfo, TableData, DatabasesDetails, Test
from .config import config_by_name

from logging.config import dictConfig
import logging.config
import yaml
logging.config.dictConfig(yaml.load(open('logging.conf')))


def create_app(config_name):
    app = FlaskAPI(__name__)
    app.config.from_object(config_by_name[config_name])

    api = Api(app, catch_all_404s=True)

    api.add_resource(Test, '/test')
    api.add_resource(AppInfo, '/')
    api.add_resource(DatabasesDetails, '/info')
    api.add_resource(TableData, '/table/<table>/data')

    return app
