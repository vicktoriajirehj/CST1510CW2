import os
import pandas as pd
from db_manager import DatabaseManager

db = DatabaseManager()

# Path to the folder where the CSV files are located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # CST1510CW2/database
CSV_DIR = os.path.join(BASE_DIR, "csv_files")           # CST1510CW2/database/csv_files

def load_csv_to_table(csv_file, table_name):
    file_path = os.path.join(CSV_DIR, csv_file)         # Full path to file
    df = pd.read_csv(file_path)
    df.to_sql(table_name, db.conn, if_exists="append", index=False)
    print(f"Loaded {csv_file} → {table_name}")

load_csv_to_table("users.csv", "users")
load_csv_to_table("cyber_incidents.csv", "cyber_incidents")
load_csv_to_table("datasets_metadata.csv", "datasets_metadata")
load_csv_to_table("it_tickets.csv", "it_tickets")

print("All sample data loaded successfully!")
db.close()
