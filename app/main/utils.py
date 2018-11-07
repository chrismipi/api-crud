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
    def correct_type(value, data_type, precision = None):
        data_type = data_type.upper()
        if "INTEGER" == data_type or "SMALLINT" == data_type:
            value = int(value)
        elif "STRING" == data_type or "CHARACTER VARYING" == data_type or "TIMESTAMP WITHOUT TIME ZONE" == data_type:
            value = str(value)
        elif "DOUBLE PRECISION" == data_type or "FLOAT" == data_type:
            value = float(value)
        return value

    @staticmethod
    def get_type(value):
        switcher = {
            "INTEGER": "int",
            "STRING": "string",
            "CHARACTER VARYING": "string",
        }
        return switcher.get(value, "string")

    @staticmethod
    def get_put_or_patch_data(fields_str, json):
        fields = fields_str.split(",")
        result = ''
        for field in fields:
            field = field.strip()

            try:
                if json[field] and field != 'id':
                    result += ", {} = '{}'".format(field, json[field])
            except KeyError:
                pass

        result = result[2:]
        return result

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
