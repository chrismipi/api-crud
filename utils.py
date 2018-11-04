class DbUtils(object):
    @staticmethod
    def get_db_tables(cur):
        cur.execute("select table_name from information_schema.tables where table_schema not in('pg_catalog', "
                    "'information_schema')")
        ver = cur.fetchall()
        tables_list = []
        for t_name in ver:
            tables_list.append(t_name[0])
        return tables_list


class Utils(object):
    @staticmethod
    def get_type(value):
        switcher = {
            "INTEGER": "int",
            "STRING": "string",
            "CHARACTER VARYING": "string",
        }
        return switcher.get(value, "string")

    @staticmethod
    def get_put_data(fields, json):

        return ""

    @staticmethod
    def get_post_data(fields_str, json):
        fields = fields_str.split(",")
        values = []
        for field in fields:
            field = field.strip()
            value = json[field]
            if value == '':
                value = None
            values.append(value)
        return values
