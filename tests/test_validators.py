import unittest
import json
from validators import Validator


class TestValidator(unittest.TestCase):

    def setUp(self):
        with open('./resources/data.json') as f:
            self.data = json.load(f)

    def test_validate_post_data_correct_data(self):
        payload = {
            "id": 2,
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
            "id": "3",
            "name": "Security Company Owner",
            "guard_name": "web",
            "created_at": "2018-10-06 10:38:08",
            "updated_at": "2018-10-06 10:38:08"
        }
        fields = self.data["tables_info"]["roles"]
        validator = Validator()

        validator.validate_post_data(fields, payload)

        self.assertEqual(1, len(validator.get_errors()), "Errors list is supposed to have length of zero")
        error = validator.get_errors()
        self.assertEqual("id", error["field"], "Errors list is supposed to have length of zero")
        self.assertEqual("wrong type", error["field"], "Errors list is supposed to have length of zero")


if __name__ == '__main__':
    unittest.main()
