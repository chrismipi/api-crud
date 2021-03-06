import psycopg2
from flask_restful import Resource
from flask import request
from flask_api import status
import sys
import json

from app.main.global_variables import DbDetails, Files
from app.main.utils import Utils as Helpers, Utils
from app.main.validators import Validators


class Test(Resource):
    def get(self):
        data = {"name": "Chris", "surname": "Mahlasela"}

        return data, status.HTTP_200_OK


class TableData(Resource):
    def __init__(self):
        self.__ok_message = "ok"
        self.__created_message = "created"

    def get(self, table):
        con = None
        response = {}
        try:
            fields = ''
            files = Files()
            with open(files.db_file) as f:
                data = json.load(f)
                data_types = []
                if data["table_names"].__contains__(table):
                    for field in data["tables_info"][table]:
                        fields += ", %s" % field["column_name"]
                        data_types.append(field["data_type"])

                    fields = fields[1:]
                    db_detail = DbDetails()
                    con = psycopg2.connect(host=db_detail.host, port=db_detail.port, database=db_detail.name,
                                           user=db_detail.username, password=db_detail.password)
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
                            row[col] = Utils.correct_type(item[i], data_types[i])
                        data.append(row)
                    response["data"] = data
                    response["message"] = self.__ok_message
                    response["status"] = status.HTTP_200_OK
                else:
                    response["error"] = "table name '%s' not found" % table
                    response["status"] = status.HTTP_404_NOT_FOUND
        except psycopg2.DatabaseError as e:
            response["error"] = str(e)
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            if con:
                con.close()
        return response, response["status"]

    def patch(self, table):
        response = {}
        if request.is_json:
            files = Files()
            with open(files.db_file) as f:
                data = json.load(f)
                if data["table_names"].__contains__(table):
                    fields = ''
                    for field in data["tables_info"][table]:
                        fields += ", {}".format(field["column_name"])
                    fields = fields[1:].strip()

                    content = request.get_json()
                    values = Helpers.get_put_or_patch_data(fields, content)

                    query_string = "update {} set {} where id = {}".format(table, values, int(content["id"]))

                    con = None
                    try:
                        db_detail = DbDetails()
                        con = psycopg2.connect(host=db_detail.host, port=db_detail.port, database=db_detail.name,
                                               user=db_detail.username, password=db_detail.password)
                        cur = con.cursor()
                        cur.execute(query_string)
                        con.commit()

                        response["message"] = self.__ok_message
                        response["status"] = status.HTTP_200_OK
                    except psycopg2.DatabaseError as e:
                        response["error"] = str(e)
                        response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                    finally:
                        if con:
                            con.close()
        else:
            response["error"] = "Only JSON is supported"
            response["status"] = status.HTTP_400_BAD_REQUEST

        return response, response["status"]

    def post(self, table):
        response = {}
        if request.is_json:
            content = request.get_json()

            files = Files()
            with open(files.db_file) as f:
                data = json.load(f)
                if data["table_names"].__contains__(table):
                    fields = data["tables_info"][table]
                    validator = Validators()

                    validator.validate_post_data(fields, content)
                    if validator.is_valid():
                        fields = ''
                        for field in data["tables_info"][table]:
                            if field["column_name"] != 'id':
                                fields += ", %s" % field["column_name"]
                        fields = fields[1:].strip()

                        values = Helpers.get_post_data(fields, content)
                        query_string = "insert into %s (%s) values %s" % (table, fields, tuple(values))
                        con = None
                        try:
                            db_detail = DbDetails()
                            con = psycopg2.connect(host=db_detail.host, port=db_detail.port, database=db_detail.name,
                                                   user=db_detail.username, password=db_detail.password)
                            cur = con.cursor()
                            cur.execute(query_string)
                            con.commit()

                            response["status"] = status.HTTP_201_CREATED
                            response["message"] = self.__created_message
                        except psycopg2.DatabaseError as e:
                            response["error"] = str(e)
                            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                        finally:
                            if con:
                                con.close()
                    else:
                        response["error"] = validator.get_errors()
                        response["status"] = status.HTTP_400_BAD_REQUEST
        else:
            response["error"] = "Only JSON is supported"
            response["status"] = status.HTTP_400_BAD_REQUEST

        return response, response["status"]

    def put(self, table):
        response = {}
        if request.is_json:
            files = Files()
            content = request.get_json()
            with open(files.db_file) as f:
                data = json.load(f)
                if data["table_names"].__contains__(table):
                    fields = data["tables_info"][table]
                    validator = Validators()

                    validator.validate_put_data(fields, content)
                    if validator.is_valid():
                        fields = ''
                        for field in data["tables_info"][table]:
                            fields += ", {}".format(field["column_name"])
                        fields = fields[1:].strip()

                        values = Helpers.get_put_or_patch_data(fields, content)

                        query_string = "update {} set {} where id = {}".format(table, values, int(content["id"]))

                        con = None
                        try:
                            db_detail = DbDetails()
                            con = psycopg2.connect(host=db_detail.host, port=db_detail.port, database=db_detail.name,
                                                   user=db_detail.username, password=db_detail.password)
                            cur = con.cursor()
                            cur.execute(query_string)
                            con.commit()

                            response["message"] = self.__ok_message
                            response["status"] = status.HTTP_200_OK
                        except psycopg2.DatabaseError as e:
                            response["error"] = str(e)
                            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                        finally:
                            if con:
                                con.close()
                    else:
                        response["error"] = validator.get_errors()
                        response["status"] = status.HTTP_400_BAD_REQUEST
        else:
            response["error"] = "Only JSON is supported"
            response["status"] = status.HTTP_400_BAD_REQUEST

        return response, response["status"]


class Databases(Resource):
    def get(self):
        con = None
        response = {}
        try:
            db_detail = DbDetails()
            con = psycopg2.connect(host=db_detail.host, port=db_detail.port, database=db_detail.name,
                                   user=db_detail.username, password=db_detail.password)
            cur = con.cursor()
            cur.execute('select datname from pg_database where datistemplate = false')
            ver = cur.fetchall()
            databases = []

            for item in ver:
                databases.append(item[0])
            response["databases"] = databases
            response["status"] = status.HTTP_200_OK
        except psycopg2.DatabaseError as e:
            response["error"] = str(e)
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            if con:
                con.close()
        return response, response["status"]


class DatabasesDetails(Resource):

    def get(self):
        con = None
        response = {}
        try:
            files = Files()
            with open(files.db_file) as f:
                data = json.load(f)
                response["database_name"] = data["database_name"]
                response["tables"] = data["table_names"]
                response["status"] = status.HTTP_200_OK
        except IOError as e:
            response["error"] = str(e)
            response["status"] = status.HTTP_400_BAD_REQUEST
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
            db_detail = DbDetails()
            con = psycopg2.connect(host=db_detail.host, port=db_detail.port, database=db_detail.name,
                                   user=db_detail.username, password=db_detail.password)
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
