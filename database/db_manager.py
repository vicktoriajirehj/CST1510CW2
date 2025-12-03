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
from db_manager import DatabaseManager

db = DatabaseManager()

def create_incident(incident_id, category, severity, status, date_reported, resolution_time):
    db.execute("""
        INSERT INTO cyber_incidents 
        (incident_id, category, severity, status, date_reported, resolution_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (incident_id, category, severity, status, date_reported, resolution_time))

def read_incidents():
    return db.fetch("SELECT * FROM cyber_incidents")

def update_incident(incident_id, new_status):
    db.execute("""
        UPDATE cyber_incidents
        SET status=?
        WHERE incident_id=?
    """, (new_status, incident_id))

def delete_incident(incident_id):
    db.execute("DELETE FROM cyber_incidents WHERE incident_id=?", (incident_id,))
