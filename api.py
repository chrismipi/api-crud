import psycopg2
import json
from flask import Flask
from flask_restful import Resource, Api
from controllers import AppInfo, Databases, DatabasesDetails, TableData
from utils import DbUtils

app = Flask(__name__)
api = Api(app)

api.add_resource(AppInfo, '/')
api.add_resource(DatabasesDetails, '/database')
api.add_resource(TableData, '/database/<table>/data')

if __name__ == '__main__':
    con = None
    response = {}
    try:
        db_name = 'test_db'
        con = psycopg2.connect(host='localhost', port='5432', database=db_name, user='test_user', password='test_password')
        cur = con.cursor()

        tables = DbUtils.getDBTables(cur)
        tables_info = {}
        for table_name in tables:
            cur.execute("select column_name, column_default, data_type, character_maximum_length from information_schema.columns WHERE table_schema=%s and table_name=%s", ('public', table_name,))          
            ver = cur.fetchall()
            fields = []
            for i in ver:
                temp = {}
                temp["column_name"] = i[0]
                temp["column_default"] = i[1]
                temp["data_type"] = i[2]
                temp["character_maximum_length"] = i[3]
                fields.append(temp)

            tables_info[table_name] = fields

        response["database_name"] = db_name
        response["table_names"] = tables
        response['tables_info'] = tables_info
        with open('data.json', 'w') as fp:
            json.dump(response, fp)

        app.run(debug=True)
    except psycopg2.DatabaseError as e:
        print(str(e))
    finally:
        if con:
            con.close()
    
    