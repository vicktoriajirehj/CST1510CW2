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

# --------------------
# DATASETS CRUD
# --------------------

def create_dataset(dataset_name, department, num_rows, file_size_mb, upload_date):
    db.execute("""
        INSERT INTO datasets_metadata 
        (dataset_name, department, num_rows, file_size_mb, upload_date)
        VALUES (?, ?, ?, ?, ?)
    """, (dataset_name, department, num_rows, file_size_mb, upload_date))


def read_datasets():
    return db.fetch("SELECT * FROM datasets_metadata")


def update_dataset_size(dataset_name, new_size):
    db.execute("""
        UPDATE datasets_metadata 
        SET file_size_mb=?
        WHERE dataset_name=?
    """, (new_size, dataset_name))


def delete_dataset(dataset_name):
    db.execute("DELETE FROM datasets_metadata WHERE dataset_name=?", (dataset_name,))
# --------------------
# IT TICKETS CRUD
# --------------------

def create_ticket(ticket_id, assigned_to, status, priority, created_date, resolution_time):
    db.execute("""
        INSERT INTO it_tickets
        (ticket_id, assigned_to, status, priority, created_date, resolution_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ticket_id, assigned_to, status, priority, created_date, resolution_time))


def read_tickets():
    return db.fetch("SELECT * FROM it_tickets")


def update_ticket_status(ticket_id, new_status):
    db.execute("""
        UPDATE it_tickets 
        SET status=?
        WHERE ticket_id=?
    """, (new_status, ticket_id))


def delete_ticket(ticket_id):
    db.execute("DELETE FROM it_tickets WHERE ticket_id=?", (ticket_id,))

