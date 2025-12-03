import sqlite3

class DatabaseManager:
    def __init__(self, db_name="platform.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE with parameters."""
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch(self, query, params=None):
        """Execute SELECT query and return rows."""
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
