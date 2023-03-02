class Pipeline:
    def __init__(self, source_database, source_table, target_database, target_table, spark):
        self.source_database = source_database
        self.source_table = source_table
        self.target_database = target_database
        self.target_table = target_table
        self.spark = spark

    def query_athena(self, query: str) -> dict:
        """
        Run the query and retrieve the result
        """
        from boto3 import client

        # Create an Athena client
        athena_client = client('athena')

        # Technical debt
        query_execution_id = athena_client.start_query_execution(
            QueryString=query,
            ResultConfiguration={
                'OutputLocation': 's3://pletora-supernovae/temp/athena-results/'
            }
        )['QueryExecutionId']

        query_status = 'QUEUED'
        while query_status in ['QUEUED', 'RUNNING']:
            query_status = athena_client.get_query_execution(
                QueryExecutionId=query_execution_id)['QueryExecution']['Status']['State']

        if query_status == 'FAILED':
            raise ValueError(f'Athena query\n{query}\nFAILED')

        result = athena_client.get_query_results(
            QueryExecutionId=query_execution_id)

        return result

    def get_source_last_partitions_dirr(self) -> list:
        """
        Given a database and table from Athena, returns a list of S3 URI's for the most recent partitions.
        """

        import re
        # Explore partition to find date partition formated as YYYY-mm-dd
        i = 0
        self.date_partition = ''
        while self.date_partition == '':
            temp = self.query_athena(f"SELECT partition_{i} FROM \"{self.source_database}\".\"{self.source_table}\"")[
                'ResultSet']['Rows'][1]['Data'][0]['VarCharValue']
            if re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}', temp):
                self.date_partition = f'partition_{i}'
            i += 1

        # Extract the most recent partition value
        self.last_date_partition_value = self.query_athena(f"SELECT MAX(CAST({self.date_partition} as date)) as last_date FROM \"{self.source_database}\".\"{self.source_table}\"")[
            'ResultSet']['Rows'][1]['Data'][0]['VarCharValue']

        # Extract s3 uri from last_patition
        s3_uri = []
        for row in self.query_athena(f"SELECT \"$path\" FROM \"{self.source_database}\".\"{self.source_table}\" WHERE {self.date_partition} = '{self.last_date_partition_value}'")['ResultSet']['Rows'][1:]:
            s3_uri.append(row['Data'][0]['VarCharValue'])
        return s3_uri

    def get_source_table(self):
        """
        Gets the query_athena standard result and transform it into a spark.DataFrame
        """
        self.get_source_last_partitions_dirr()
        table_as_dict = self.query_athena(
            f"SELECT * FROM \"{self.source_database}\".\"{self.source_table}\" WHERE {self.date_partition} = '{self.last_date_partition_value}'")

        columns = [list(dict.values())[0]
                   for dict in table_as_dict['ResultSet']['Rows'][0]['Data']]

        # Creating data = [{"partition_0": "sne-2020-2024", "partition_1": "2023-02-11"}, {"partition_0": "value", "partition_1": "value1"}, ...]
        data = []
        for dict in table_as_dict['ResultSet']['Rows'][1:]:

            temp = {}
            # dict["Data"] = [{1}, {2}, {3}] ; columns = ['column1', 'column2', 'column3'] --> zip(columns, dict["Data"]) = [('column1', {1}), ('column2'), {2}, ...]
            for z in zip(columns, dict['Data']):
                temp[z[0]] = list(z[1].values())[0]

            data.append(temp)

        df = self.spark.createDataFrame(data)
        return df

    def get_bucket_name(self) -> str:
        """
        Get the name of the bucket where the table is located
        """
        self.bucket_name = self.get_source_last_partitions_dirr()[
            0].split('/')[2]
        return self.bucket_name

    def save_parquet(self, df, key: str) -> None:
        """
        target_uri: s3:// + self.bucket_name + key; key = path + file_name

        Example:
            key = '20-raw/git/{table_name}/.../partition_n/supernovae.parquet'
            target_uri = s3://{bucket_name}/20-raw/git/{table_name}/.../partition_n/{current_date}/supernovae.parquet
        """
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")

        key = key.split('/')
        key.insert(-1, today)
        key = '/'.join(key)

        self.get_bucket_name()

        target_uri = f"s3://{self.bucket_name}/{key}"
        df.write.mode('overwrite').parquet(target_uri)
        return None
