class Validator:

    def __init__(self):
        self.errors_list = []
        self.missing = "required"
        self.wrong_type = "is of the wrong type"

    def is_valid(self):
        return self.errors_list.__len__() == 0

    def get_errors(self):
        return self.errors_list

    def validate_post_data(self, fields, payload):
        for field in fields:
            if field["column_name"] in payload:
                # print(field["column_default"])
                data_type = field["data_type"]
                # print(field["column_name"])

                print("Value ", payload[field["column_name"]])
            else:
                temp = {'field': field["column_name"], 'message': self.missing}
                self.errors_list.append(temp)

        return self
