from db_manager import DatabaseManager

db = DatabaseManager()

# Users table
db.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT,
    role TEXT
)
""")

# Cybersecurity incidents
db.execute("""
CREATE TABLE IF NOT EXISTS cyber_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id TEXT,
    category TEXT,
    severity TEXT,
    status TEXT,
    date_reported TEXT,
    resolution_time INTEGER
)
""")

# Dataset metadata
db.execute("""
CREATE TABLE IF NOT EXISTS datasets_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_name TEXT,
    department TEXT,
    num_rows INTEGER,
    file_size_mb REAL,
    upload_date TEXT
)
""")

# IT tickets
db.execute("""
CREATE TABLE IF NOT EXISTS it_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT,
    assigned_to TEXT,
    status TEXT,
    priority TEXT,
    created_date TEXT,
    resolution_time INTEGER
)
""")

print("All tables created successfully!")
db.close()
