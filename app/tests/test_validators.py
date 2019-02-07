import json
import os
import random
import string
import unittest

from app.main.validators import Validators, TypeValidator, LengthValidator


class TestLengthValidator(unittest.TestCase):
    def setUp(self):
        pass

    @staticmethod
    def __random_word(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def test_none_length(self):
        value = "hi there, there is something"
        length = None

        validator = LengthValidator(length, value)
        self.assertEqual(True, validator.validate().is_valid())

    def test_255_length_incorrect(self):
        value = TestLengthValidator.__random_word(255)
        length = 254

        validator = LengthValidator(length, value)
        self.assertEqual(False, validator.validate().is_valid())

    def test_255_length_correct(self):
        value = TestLengthValidator.__random_word(255)
        length = 255

        validator = LengthValidator(length, value)
        self.assertEqual(True, validator.validate().is_valid())

    def test_255_length__less_correct(self):
        value = TestLengthValidator.__random_word(30)
        length = 255

        validator = LengthValidator(length, value)
        self.assertEqual(True, validator.validate().is_valid())


class TestTypeValidator(unittest.TestCase):
    def setUp(self):
        pass

    def test_boolean_correct(self):
        value = False
        data_type = "boolean"

        validator = TypeValidator(data_type, value)
        validator.validate()

        self.assertEqual(True, validator.is_valid())

    def test_float_correct(self):
        value = 123.23
        data_type = "float"

        validator = TypeValidator(data_type, value)
        validator.validate()

        self.assertEqual(True, validator.is_valid())

    def test_float_incorrect(self):
        value = 123
        data_type = "float"

        validator = TypeValidator(data_type, value)
        validator.validate()

        self.assertEqual(False, validator.is_valid())

    def test_integer_correct(self):
        value = 123
        data_type = "integer"

        validator = TypeValidator(data_type, value)
        validator.validate()

        self.assertEqual(True, validator.is_valid())

    def test_string_correct(self):
        value = "string"
        data_type = "character varying"

        validator = TypeValidator(data_type, value)
        validator.validate()

        self.assertEqual(True, validator.is_valid())

    def test_integer_incorrect(self):
        value = "12345"
        data_type = "integer"

        validator = TypeValidator(data_type, value)
        validator.validate()

        self.assertEqual(False, validator.is_valid())

    def test_string_incorrect(self):
        value = 123
        data_type = "character varying"

        validator = TypeValidator(data_type, value)
        validator.validate()

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
        validator = Validators()

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
        validator = Validators()

        validator.validate_post_data(fields, payload)

        self.assertEqual(1, len(validator.get_errors()), "Errors list is supposed to have length of zero")
        error = validator.get_errors()
        self.assertEqual("guard_name", error[0]["field"], "Errors list is supposed to have length of zero")
        self.assertEqual("value is of the wrong type, required type character varying", error[0]["message"],
                         "Errors list is supposed to have length of zero")


if __name__ == '__main__':
    unittest.main()
