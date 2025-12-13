import pandas as pd
import os
from database.db_manager import DatabaseManager
from models.security_incident import SecurityIncident
from models.dataset import DatasetMetadata
from models.ticket import ITTicket


db = DatabaseManager()


def get_all_incidents():
    df = pd.read_csv("database/csv_files/cyber_incidents.csv")
    return [
        SecurityIncident(
            row['incident_id'],
            row['category'],
            row['severity'],
            row['status'],
            row['date_reported'],
            row['resolution_time']
        )
        for _, row in df.iterrows()
    ]
def get_all_datasets():
    csv_path = os.path.join("database", "csv_files", "datasets_metadata.csv")
    if not os.path.exists(csv_path):
        return []  # CSV missing -> empty list

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()  # remove whitespace

    return [DatasetMetadata(
        row['dataset_name'],
        row['department'],
        row['num_rows'],
        row['file_size_mb'],
        row['upload_date']
    ) for _, row in df.iterrows()]


def get_all_tickets():
    df = pd.read_csv("database/csv_files/it_tickets.csv")
    df.columns = df.columns.str.strip()
    return [ITTicket(row['ticket_id'], row['assigned_to'], row['status'], row['priority'], row['created_date'], row['resolution_time'])
            for _, row in df.iterrows()]
