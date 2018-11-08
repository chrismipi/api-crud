import os


class DbDetails(object):
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.name = os.getenv('DB_NAME')
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')

    def get_connection_str(self):
        return "{}:{}".format(self.host, self.port)
