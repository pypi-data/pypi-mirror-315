
import duckdb
import tabulate
import pandas as pd
from .bigquery_to_pandas import BigQueryToPandas


class InteractionService:
    def __init__(self, project_id):
        """
        Initializes the InteractionService with BigQuery and DuckDB.

        Args:
            project_id (str): Google Cloud project ID.
        """
        self.project_id = project_id
        self.bigquery_to_pandas = BigQueryToPandas(project_id)
        self.duckdb_connection = duckdb.connect()

    def load_data_to_duckdb(self, table_name, filters=None, duckdb_table_name='temp_table'):
        """
        Loads data from a BigQuery table, applies filtering, and registers it in DuckDB.

        Args:
            table_name (str): The name of the BigQuery table in `project.dataset.table` format.
            filters (dict): Dictionary of filters to apply to the data.
            duckdb_table_name (str): Name to register the table in DuckDB. Default is 'temp_table'.

        Returns:
            pd.DataFrame: DataFrame of the loaded and filtered data.
        """
        df = self.bigquery_to_pandas.load_bigquery_table(table_name, filters)
        df = self.bigquery_to_pandas.convert_data_types(df)

        self.duckdb_connection.register(duckdb_table_name, df)
        return df

    def run_duckdb_query(self, query):
        """
        Executes a query on the DuckDB connection.

        Args:
            query (str): SQL query to run on DuckDB.

        Returns:
            pd.DataFrame: DataFrame containing the query results.
        """
        result_df = self.duckdb_connection.execute(query).fetchdf()
        return result_df

    def display_query_results(self, query):
        """
        Executes a query on DuckDB and displays the results using IPython.

        Args:
            query (str): SQL query to run on DuckDB.
        """
        result_df = self.run_duckdb_query(query)
        print(tabulate.tabulate(result_df, headers="keys", tablefmt="pretty"))
