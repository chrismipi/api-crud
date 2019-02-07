class BaseValidator(object):
    def __init__(self, value):
        self._value = value
        self._valid = False

    def is_valid(self):
        raise NotImplementedError("Should have implemented this")

    def validate(self):
        raise NotImplementedError("Should have implemented this")


class LengthValidator(BaseValidator):
    def __init__(self, length, value):
        super(LengthValidator, self).__init__(value)
        self.__length = length

    def is_valid(self):
        return self._valid

    def validate(self):
        value = str(self._value)
        if isinstance(self.__length, type(1)) or isinstance(self.__length, type(0.1)):
            self._valid = len(value) <= self.__length
        else:
            self._valid = True
        return self


class TypeValidator(BaseValidator):
    def __init__(self, data_type, value):
        super(TypeValidator, self).__init__(value)
        self.__data_type = data_type

    def is_valid(self):
        return self._valid

    def __get_type(self):
        switcher = {
            "BOOLEAN": type(False),  # boolean
            "INTEGER": type(1),  # integer
            "SMALLINT": type(1),  # integer
            "FLOAT": type(0.2),  # float
            "DOUBLE PRECISION": type(0.2),  # float
            "STRING": type("string"),  # string
            "TEXT": type("string"),  # string
            "CHARACTER VARYING": type("string"),  # string
            "TIMESTAMP WITHOUT TIME ZONE": type("string"),  # string
        }

        return switcher.get(str(self.__data_type).upper(), None)

    def validate(self):
        actual_type = self.__get_type()
        value_type = type(self._value)
        if value_type == actual_type:
            self._valid = True

        return self


class Validators(object):
    def __init__(self):
        self.__errors_list = []
        self.__missing = "required"
        self.__wrong_type = "value is of the wrong type"
        self.__wrong_length = "value is of the wrong length"

    def is_valid(self):
        return self.__errors_list.__len__() == 0

    def get_errors(self):
        return self.__errors_list

    def validate_patch_data(self, fields, payload):
        pass

    def validate_put_data(self, fields, payload):
        pass

    def validate_post_data(self, fields, payload):
        for field in fields:
            if field["column_name"] != "id":
                # validating the field types
                if field["column_name"] in payload:
                    # print(field["column_default"])
                    data_type = field["data_type"]
                    column_name = field["column_name"]
                    value = payload[field["column_name"]]
                    type_validator = TypeValidator(data_type, value)
                    type_validator.validate()
                    if not type_validator.is_valid():
                        temp = {'field': column_name,
                                'message': "{}, required type {}".format(self.__wrong_type, data_type)}
                        self.__errors_list.append(temp)

                    data_length = field["character_maximum_length"]
                    length_validator = LengthValidator(data_length, value)
                    length_validator.validate()

                    if not length_validator.is_valid():
                        temp = {'field': column_name,
                                'message': "{}, required length {}".format(self.__wrong_length, data_length)}
                        self.__errors_list.append(temp)

                else:
                    temp = {'field': field["column_name"], 'message': self.__missing}
                    self.__errors_list.append(temp)

        return self
