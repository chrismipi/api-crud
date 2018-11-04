import unittest
from utils import Utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

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
