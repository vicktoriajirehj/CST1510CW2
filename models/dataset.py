class DatasetMetadata:
    def __init__(self, name, department, num_rows, size_mb, upload_date):
        self.name = name
        self.department = department
        self.num_rows = num_rows
        self.size_mb = size_mb
        self.upload_date = upload_date
    def update_size(self, new_size):
        self.size_mb = new_size
