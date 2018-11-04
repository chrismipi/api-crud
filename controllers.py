import psycopg2
from flask_restful import Resource
from flask import request
import sys
import json
from utils import Utils as Helpers


class TableData(Resource):
    def get(self, table):
        con = None
        response = {}
        dbname = 'test_db'
        try:
            fields = ''
            with open('data.json') as f:
                data = json.load(f)

                if data["table_names"].__contains__(table):
                    for field in data["tables_info"][table]:
                        fields += ", %s" % field["column_name"]
                    fields = fields[1:]
                    con = psycopg2.connect(host='localhost', port='5432', database=dbname, user='test_user',
                                           password='test_password')
                    cur = con.cursor()
                    query_string = "select %s from %s" % (fields, table)
                    cur.execute(query_string)
                    ver = cur.fetchall()
                    data = []
                    columns = fields.split(",")
                    for item in ver:
                        row = {}
                        for i, col in enumerate(columns):
                            col = col.strip(' ')
                            row[col] = str(item[i])
                        data.append(row)
                    response["data"] = data
                    response["status"] = 200
                else:
                    response["error"] = "table name '%s' not found" % table
                    response["status"] = 404
        except psycopg2.DatabaseError as e:
            response["error"] = str(e)
            response["status"] = 500
        finally:
            if con:
                con.close()
        return response, response["status"]

    def put(self, table):
        dbname = 'test_db'
        response = {}
        if request.is_json:
            with open('data.json') as f:
                data = json.load(f)
                if data["table_names"].__contains__(table):
                    fields = ''
                    for field in data["tables_info"][table]:
                        fields += ", %s" % field["column_name"]
                    fields = fields[1:].strip()

                    content = request.get_json()
                    values = Helpers.get_put_or_patch_data(fields, content)

                    query_string = "update {} set {} where id = {}".format(table, values, int(content["id"]))

                    print(query_string)
                    con = None
                    try:
                        con = psycopg2.connect(host='localhost', port='5432', database=dbname, user='test_user',
                                               password='test_password')
                        cur = con.cursor()
                        cur.execute(query_string)
                        con.commit()

                        response["message"] = "Good"
                        response["status"] = 200
                    except psycopg2.DatabaseError as e:
                        response["error"] = str(e)
                        response["status"] = 500
                    finally:
                        if con:
                            con.close()
        else:
            response["error"] = "Only JSON is supported"
            response["status"] = 400

        return response, response["status"]

    def post(self, table):
        dbname = 'test_db'
        response = {}
        if request.is_json:
            with open('data.json') as f:
                data = json.load(f)
                if data["table_names"].__contains__(table):
                    fields = ''
                    for field in data["tables_info"][table]:
                        if field["column_name"] != 'id':
                            fields += ", %s" % field["column_name"]
                    fields = fields[1:].strip()

                    content = request.get_json()
                    values = Helpers.get_post_data(fields, content)
                    query_string = "insert into %s (%s) values %s" % (table, fields, tuple(values))
                    con = None
                    try:
                        con = psycopg2.connect(host='localhost', port='5432', database=dbname, user='test_user',
                                               password='test_password')
                        cur = con.cursor()
                        cur.execute(query_string)
                        con.commit()

                        response["status"] = 200
                    except psycopg2.DatabaseError as e:
                        response["error"] = str(e)
                        response["status"] = 500
                    finally:
                        if con:
                            con.close()
        else:
            response["error"] = "Only JSON is supported"
            response["status"] = 400

        return response, response["status"]


class Databases(Resource):
    def get(self):
        con = None
        response = {}
        try:
            con = psycopg2.connect(host='localhost', port='5432', database='test_db', user='test_user',
                                   password='test_password')
            cur = con.cursor()
            cur.execute('select datname from pg_database where datistemplate = false')
            ver = cur.fetchall()
            databases = []

            for item in ver:
                databases.append(item[0])
            response["databases"] = databases
            response["status"] = 200
        except psycopg2.DatabaseError as e:
            response["error"] = str(e)
            response["status"] = 500
        finally:
            if con:
                con.close()
        return response, response["status"]


class DatabasesDetails(Resource):

    def get(self):
        con = None
        response = {}
        try:
            with open('data.json') as f:
                data = json.load(f)
                response["database_name"] = data["database_name"]
                response["tables"] = data["table_names"]
                response["status"] = 200
        except IOError as e:
            response["error"] = str(e)
            response["status"] = 400
        finally:
            if con:
                con.close()
        return response, response["status"]


class AppInfo(Resource):

    def get(self):
        con = None
        version = 'api-crud v.0.0.1'
        response = {
            "application_name": version,
        }
        try:
            con = psycopg2.connect(host='localhost', port='5432', database='test_db', user='test_user',
                                   password='test_password')
            cur = con.cursor()
            cur.execute('select version()')
            ver = cur.fetchone()
            response['database_info'] = ver[0]
        except psycopg2.DatabaseError as e:
            print('Error %s' % e)
            sys.exit(1)
        finally:
            if con:
                con.close()
        return response
