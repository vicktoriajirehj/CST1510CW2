import pandas as pd
from db_manager import DatabaseManager

db = DatabaseManager()

def load_csv_to_table(csv_file, table_name):
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, db.conn, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into {table_name}")

# Example — adjust file names to match your downloaded CSVs
load_csv_to_table("cyber_incidents.csv", "cyber_incidents")
load_csv_to_table("datasets_metadata.csv", "datasets_metadata")
load_csv_to_table("it_tickets.csv", "it_tickets")

db.close()
