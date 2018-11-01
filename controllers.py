import psycopg2
from flask_restful import Resource
from flask import request
import sys
import json

class DatabasesData(Resource):
  def get(self, dbname, table):
    con = None
    response = {}
    try:
      fields = ''
      with open('data.json') as f:
        data = json.load(f)
        for field in data["fields"]: fields += ", %s" % field["column_name"]
        fields = fields[1:]
      con = psycopg2.connect(host='localhost', port='5432', database=dbname, user='test_user', password='test_password') 
      cur = con.cursor()
      query_string = "select %s from %s" % (fields, table)
      cur.execute(query_string)          
      ver = cur.fetchall()
      data = []
      coloums = fields.split(",")
      for item in ver:
        row = {}
        for i, col in enumerate(coloums):
          col = col.strip(' ')
          row[col] = str(item[i])
        data.append(row)

      response["data"] = data
      response["status"] = 200
    except psycopg2.DatabaseError as e:
      response["error"] = str(e)
      response["status"] = 500
    finally:
        if con:
            con.close()
    return response, response["status"]

  def post(self, dbname):
    response = {}
    if request.is_json:
      content = request.get_json()
      response["message"] = content
      response["status"] = 200
    else:
      response["error"] = "Only JSON is supported"
      response["status"] = 400
    
    return response, response["status"]

class Databases(Resource):
  def get(self):
      con = None
      response = {}
      try:
          con = psycopg2.connect(host='localhost', port='5432', database='postgres', user='test_user', password='test_password')
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
    def get(self, dbname):
      con = None
      response = {}
      try:
        con = psycopg2.connect(host='localhost', port='5432', database=dbname, user='test_user', password='test_password')
        cur = con.cursor()
        cur.execute("select column_name, column_default, data_type, character_maximum_length FROM information_schema.columns WHERE table_schema=%s and table_name=%s", ('public', dbname,))          
        ver = cur.fetchall()
        fields = []
        for i in ver:
            temp = {}
            temp["column_name"] = i[0]
            temp["column_default"] = i[1]
            temp["data_type"] = i[2]
            temp["character_maximum_length"] = i[3]
            fields.append(temp)

        response["database_name"] = dbname
        response["fields"] = fields
        response["status"]= 200
      except psycopg2.DatabaseError as e:
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
        con = psycopg2.connect(host='localhost', port='5432', database='test_db', user='test_user', password='test_password')
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