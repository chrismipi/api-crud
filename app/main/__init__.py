from flask import Flask
from flask_restful import Api

from app.main.controllers import AppInfo, TableData, DatabasesDetails, Test
from .config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    api = Api(app)

    api.add_resource(Test, '/test')
    api.add_resource(AppInfo, '/')
    api.add_resource(DatabasesDetails, '/database')
    api.add_resource(TableData, '/database/<table>/data')

    return app
