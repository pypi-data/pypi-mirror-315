
from google.cloud import bigquery


class BigQueryClient:
    def __init__(self, project_id):
        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)

    def run_query(self, query):
        query_job = self.client.query(query)
        result = query_job.result()
        rows = [dict(row) for row in result]
        return rows
