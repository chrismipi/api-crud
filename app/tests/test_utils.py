import unittest
from app.main.utils import Utils


class TestUtils(unittest.TestCase):
    data = None

    def setUp(self):
        pass

    def test_type_corrector(self):
        data_type = "INTEGER"
        value = "345678"
        result = Utils.correct_type(value, data_type)

        self.assertEqual(345678, result, "Type is supposed to be an integer")

    def test_get_type_string(self):
        result = Utils.get_type("String")
        self.assertEqual("string", result)

    def test_get_type_char(self):
        result = Utils.get_type("CHARACTER VARYING")
        self.assertEqual("string", result)

    def test_get_type_int(self):
        result = Utils.get_type("INTEGER")
        self.assertEqual("int", result)


if __name__ == '__main__':
    unittest.main()
