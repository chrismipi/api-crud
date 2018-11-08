import psycopg2

import json
import os
import unittest
from dotenv import load_dotenv

from app.main import create_app
from flask_script import Manager

from app.main.utils import DbUtils
from app.main.global_variables import DbDetails

# load .env file
app_root = os.path.join(os.path.dirname(__file__), '.')
dot_env_path = os.path.join(app_root, '.env')
load_dotenv(dot_env_path)

app = create_app(os.getenv('APP_ENV') or 'dev')
app.app_context().push()

manager = Manager(app)


@manager.command
def run():
    app.run(debug=app.config["DEBUG"])


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/tests', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    con = None
    response = {}
    try:
        db_detail = DbDetails()
        con = psycopg2.connect(host=db_detail.host, port=db_detail.port, database=db_detail.name,
                               user=db_detail.username, password=db_detail.password)
        cur = con.cursor()

        tables = DbUtils.get_db_tables(cur)
        tables_info = {}
        for table_name in tables:
            cur.execute("select column_name, column_default, data_type, character_maximum_length from "
                        "information_schema.columns WHERE table_schema=%s and table_name=%s", ('public', table_name,))
            ver = cur.fetchall()
            fields = []
            for i in ver:
                temp = {"column_name": i[0], "column_default": i[1], "data_type": i[2],
                        "character_maximum_length": i[3]}
                fields.append(temp)

            tables_info[table_name] = fields

        response["database_name"] = db_detail.name
        response["table_names"] = tables
        response['tables_info'] = tables_info
        with open('data.json', 'w') as fp:
            json.dump(response, fp)

        manager.run()
    except psycopg2.DatabaseError as e:
        print(str(e))
    finally:
        if con:
            con.close()

