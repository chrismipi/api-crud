import psycopg2
from flask_restful import Resource

class Databases(Resource):
    def get(self):
        con = None
        response = {}
        try:
            con = psycopg2.connect(host='localhost', port='54321', database='postgres', user='ping_management_user', password='ping_management_password') 
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
        con = psycopg2.connect(host='localhost', port='54321', database=dbname, user='ping_management_user', password='ping_management_password') 
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
        con = psycopg2.connect(host='localhost', port='54321', database='ping_management', user='ping_management_user', password='ping_management_password') 
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