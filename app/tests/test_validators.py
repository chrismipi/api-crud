import unittest
import json
import os
from app.main.validators import Validator, TypeValidator


class TestTypeValidator(unittest.TestCase):
    def setUp(self):
        pass

    def test_boolean_correct(self):
        value = False
        data_type = "boolean"

        validator = TypeValidator(data_type, value)
        validator.validate_type()

        self.assertEqual(True, validator.is_valid())

    def test_float_correct(self):
        value = 123.23
        data_type = "float"

        validator = TypeValidator(data_type, value)
        validator.validate_type()

        self.assertEqual(True, validator.is_valid())

    def test_float_incorrect(self):
        value = 123
        data_type = "float"

        validator = TypeValidator(data_type, value)
        validator.validate_type()

        self.assertEqual(False, validator.is_valid())

    def test_integer_correct(self):
        value = 123
        data_type = "integer"

        validator = TypeValidator(data_type, value)
        validator.validate_type()

        self.assertEqual(True, validator.is_valid())

    def test_string_correct(self):
        value = "string"
        data_type = "character varying"

        validator = TypeValidator(data_type, value)
        validator.validate_type()

        self.assertEqual(True, validator.is_valid())

    def test_integer_incorrect(self):
        value = "12345"
        data_type = "integer"

        validator = TypeValidator(data_type, value)
        validator.validate_type()

        self.assertEqual(False, validator.is_valid())

    def test_string_incorrect(self):
        value = 123
        data_type = "character varying"

        validator = TypeValidator(data_type, value)
        validator.validate_type()

        self.assertEqual(False, validator.is_valid())


class TestValidator(unittest.TestCase):

    def setUp(self):
        path = os.path.join('app', 'tests', 'resources', 'data.json')
        with open(path) as f:
            self.data = json.load(f)

    def test_validate_post_data_correct_data(self):
        payload = {
            "name": "Security Company Owner",
            "guard_name": "web",
            "created_at": "2018-10-06 10:38:08",
            "updated_at": "2018-10-06 10:38:08"
        }
        fields = self.data["tables_info"]["roles"]
        validator = Validator()

        validator.validate_post_data(fields, payload)

        self.assertEqual(0, len(validator.get_errors()), "Errors list is supposed to have length of zero")

    def test_validate_post_data_correct_data_type_wrong(self):
        payload = {
            "name": "Security Company Owner",
            "guard_name": 123,
            "created_at": "2018-10-06 10:38:08",
            "updated_at": "2018-10-06 10:38:08"
        }
        fields = self.data["tables_info"]["roles"]
        validator = Validator()

        validator.validate_post_data(fields, payload)

        self.assertEqual(1, len(validator.get_errors()), "Errors list is supposed to have length of zero")
        error = validator.get_errors()
        self.assertEqual("guard_name", error[0]["field"], "Errors list is supposed to have length of zero")
        self.assertEqual("value is of the wrong type, required type character varying", error[0]["message"],
                         "Errors list is supposed to have length of zero")


if __name__ == '__main__':
    unittest.main()
