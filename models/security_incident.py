class SecurityIncident:
    def __init__(self, incident_id, category, severity, status, date_reported, resolution_time):
        self.incident_id = incident_id
        self.category = category
        self.status = status
        self.date_reported =date_reported
        self.resolution_time = resolution_time

    def update_status(self, new_status):
        self.status = new_status
