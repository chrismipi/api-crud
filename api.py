import psycopg2
import json
from flask import Flask
from flask_restful import Resource, Api
from controllers import AppInfo, Databases, DatabasesDetails, DatabasesData

app = Flask(__name__)
api = Api(app)

api.add_resource(AppInfo, '/')
api.add_resource(Databases, '/databases')
api.add_resource(DatabasesDetails, '/database/<dbname>')
api.add_resource(DatabasesData, '/database/<dbname>/data')

if __name__ == '__main__':
    con = None
    response = {}
    try:
        con = psycopg2.connect(host='localhost', port='54321', database='ping_management', user='ping_management_user', password='ping_management_password') 
        cur = con.cursor()
        cur.execute("select column_name, column_default, data_type, character_maximum_length FROM information_schema.columns WHERE table_schema=%s and table_name=%s", ('public', 'ping_management',))          
        ver = cur.fetchall()
        fields = []
        for i in ver:
            temp = {}
            temp["column_name"] = i[0]
            temp["column_default"] = i[1]
            temp["data_type"] = i[2]
            temp["character_maximum_length"] = i[3]
            fields.append(temp)

        response["database_name"] = 'ping_management'
        response["fields"] = fields
        f = open("demofile.json", "w")
        f.write(str(fields))
        with open('data.json', 'w') as fp:
            json.dump(response, fp)

        app.run(debug=True)
    except psycopg2.DatabaseError as e:
        print(str(e))
    finally:
        if con:
            con.close()
    
    