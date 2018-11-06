from flask import Flask
from flask_restful import Api
from app.main.controllers import AppInfo, DatabasesDetails, TableData

blueprint = Flask(__name__)
blueprint.config.from_object('config')
api = Api(blueprint)

api.add_resource(AppInfo, '/')
api.add_resource(DatabasesDetails, '/database')
api.add_resource(TableData, '/database/<table>/data')

