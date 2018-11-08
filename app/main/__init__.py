from flask_restful import Api
from flask_api import FlaskAPI

from app.main.controllers import AppInfo, TableData, DatabasesDetails, Test
from .config import config_by_name
from flask import got_request_exception


def log_exception(sender, exception, **extra):
    """ Log an exception to our logging framework """
    sender.logger.debug(':> Got exception during processing: %s', exception)


def create_app(config_name):
    app = FlaskAPI(__name__)
    app.config.from_object(config_by_name[config_name])

    got_request_exception.connect(log_exception, app)
    api = Api(app, catch_all_404s=True)

    api.add_resource(Test, '/test')
    api.add_resource(AppInfo, '/')
    api.add_resource(DatabasesDetails, '/database')
    api.add_resource(TableData, '/database/<table>/data')

    return app
