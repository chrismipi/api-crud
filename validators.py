class TypeValidator(object):
    def __init__(self, data_type, value):
        self.data_type = data_type
        self.value = value
        self.valid = False

    def is_valid(self):
        return self.valid

    def __get_type(self):
        switcher = {
            "INTEGER": type(1),  # integer
            "STRING": type("string"),  # string
            "CHARACTER VARYING": type("string"),  # string
            "TIMESTAMP WITHOUT TIME ZONE": type("string"),  # string
        }

        return switcher.get(str(self.data_type).upper(), None)

    def validate_type(self):
        actual_type = self.__get_type()
        value_type = type(self.value)
        if value_type == actual_type:
            self.valid = True


class Validator(object):
    def __init__(self):
        self.errors_list = []
        self.missing = "required"
        self.wrong_type = "value is of the wrong type"

    def is_valid(self):
        return self.errors_list.__len__() == 0

    def get_errors(self):
        return self.errors_list

    def validate_post_data(self, fields, payload):
        for field in fields:
            if field["column_name"] in payload:
                # print(field["column_default"])
                data_type = field["data_type"]
                value = payload[field["column_name"]]
                type_validator = TypeValidator(data_type, value)
                type_validator.validate_type()
                if not type_validator.is_valid():
                    temp = {'field': field["column_name"], 'message': "{}, required type {}".format(self.wrong_type,
                                                                                                    data_type)}
                    self.errors_list.append(temp)
            else:
                temp = {'field': field["column_name"], 'message': self.missing}
                self.errors_list.append(temp)

        return self
