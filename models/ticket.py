class ITTicket:
    def __init__(self, ticket_id, assigned_to, status, priority, created_date, resolution_time):
        self.ticket_id = ticket_id
        self.assigned_to = assigned_to
        self.status = status
        self.priority = priority
        self.created_date = created_date
        self.resolution_time = resolution_time
    def update_status(self, new_status):
        self.status = new_status

