class DbCredentials(object):
    def __init__(self, db, username, password):
        self.db = db
        self.user = username
        self.password = password
