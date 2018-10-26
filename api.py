from flask import Flask
from flask_restful import Resource, Api
from controllers import AppInfo, Databases, DatabasesDetails
import sys

app = Flask(__name__)
api = Api(app)

api.add_resource(AppInfo, '/')
api.add_resource(Databases, '/databases')
api.add_resource(DatabasesDetails, '/database/<dbname>')

if __name__ == '__main__':
    app.run(debug=True)