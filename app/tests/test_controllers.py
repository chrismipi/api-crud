import json

from app.tests.base import BaseTestCase


class TestExample(BaseTestCase):

    def test_get(self):
        resp_register = self.client.get('/test',)
        data_register = json.loads(resp_register.data.decode())

        self.assertEqual(data_register["name"], "Chris")
        self.assertEqual(data_register["surname"], "Mahlasela")
