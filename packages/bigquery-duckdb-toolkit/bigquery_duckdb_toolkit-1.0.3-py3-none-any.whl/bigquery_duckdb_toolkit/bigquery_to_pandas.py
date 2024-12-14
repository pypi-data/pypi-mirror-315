import google.auth
import pandas as pd
from google.cloud import bigquery


class BigQueryToPandas:
    def __init__(self, project_id):
        credentials, project = google.auth.default()
        self.client = bigquery.Client(credentials=credentials, project=project_id)

    def get_partition_column(self, table_name):
        """
        Retrieves the partition column of a BigQuery table using INFORMATION_SCHEMA.

        Args:
            table_name (str): Name of the table in the format `project.dataset.table`.

        Returns:
            str: The name of the partition column, or None if no partitioning is found.
        """
        project_id, dataset_id, table_id = table_name.split('.')
        query = f"""
        SELECT column_name
        FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
        WHERE table_name = '{table_id}' AND is_partitioning_column = 'YES'
        """
        result = self.client.query(query).result()
        partition_column = next((row['column_name'] for row in result), None)
        return partition_column

    def load_bigquery_table(self, table_name, filters):
        """
        Loads data from a BigQuery table into a pandas DataFrame with dynamic filtering.

        Args:
            table_name (str): Name of the table in the format `project.dataset.table`.
            filters (dict): Dictionary containing filters, where keys are column names and values are filter values.

        Returns:
            pd.DataFrame: DataFrame containing the filtered table data.
        """
        partition_column = self.get_partition_column(table_name)

        where_conditions = []
        for column, value in filters.items():
            if column == "date" and partition_column:
                where_conditions.append(f"DATE({partition_column}) = '{value}'")
            else:
                where_conditions.append(f"CAST({column} AS STRING) = '{value}'")

        where_clause = " AND ".join(where_conditions)

        query = f"""
        SELECT *
        FROM `{table_name}`
        WHERE {where_clause}
        """
        df = self.client.query(query).to_dataframe()
        return df

    def filter_dataframe(self, df):
        """
        Applies custom filters to the DataFrame. This method can be expanded as needed.

        Args:
            df (pd.DataFrame): DataFrame to be filtered.

        Returns:
            pd.DataFrame: Filtered DataFrame.
        """
        return df

    def convert_data_types(self, df):
        """
        Converts specific data types in the DataFrame, adjusting datetime for timezone and dbdate to string.

        Args:
            df (pd.DataFrame): DataFrame to have data types adjusted.

        Returns:
            pd.DataFrame: DataFrame with converted data types.
        """
        for column in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                if df[column].dtype.tz is not None:
                    df[column] = df[column].dt.tz_localize(None)
                df[column] = df[column].astype('datetime64[ns]')
            elif df[column].dtype.name == 'dbdate':
                df[column] = df[column].astype(str)

        return df
