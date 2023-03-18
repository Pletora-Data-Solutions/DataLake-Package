class Pipeline:
    def __init__(self, source_database, source_table, target_database, target_table, spark):
        self.source_database = source_database
        self.source_table = source_table
        self.target_database = target_database
        self.target_table = target_table
        self.spark = spark
        
    def query_athena(self, query: str) -> dict:
        """
        Streams the results of a single query execution from the Athena query results location in Amazon S3. 
        This request does not execute the query but returns results.
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
            query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)['QueryExecution']['Status']['State']
        
        if query_status == 'FAILED':
            raise ValueError(f'Athena query FAILED.')
    
        result = athena_client.get_query_results(QueryExecutionId=query_execution_id)

        return result
        
    def check_table_exists(self, database: str, table: str) -> bool:
        """Check if table exists in database."""
        
        from boto3 import client
        
        # Create an Athena client
        athena_client = client('athena')
        
        try:
            response = athena_client.get_table_metadata(
                CatalogName='AwsDataCatalog',
                DatabaseName=database,
                TableName=table
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'MetadataException':
                return False
            else:
                raise e
            
    def get_source_partition(self) -> SparkDataFrame:
        """
        Given a database and table from Athena, returns a SparkDataFrame with partitions general informations.
        """
        from boto3 import client
        glue_client = client('glue')
        
        try:
            response = glue_client.get_partitions(
                                    DatabaseName = self.source_database, 
                                    TableName = self.source_table
                                    )
        except ClientError as e:
            raise e
        
        data = []
        for partition in response['Partitions']:
            row = [v for v in partition['Values']] + [partition['CreationTime'], partition['StorageDescriptor']['Location']]
            data.append(row)
            schema = [f"partition_{n}" for n in range(len(partition['Values']))] + ['CreationTime', 'Location']
        return self.spark.createDataFrame(data, schema)
        
        
    def get_source_last_partitions(self) -> SparkDataFrame:
        """
        GroupBy partitions SparkDataFrame for the max(CreationTime) returning a SparkDataFrame with each partition max load date
        """
        df = self.get_source_partition()
        
        import re
        # Explore partition to find date partition formated as YYYY-mm-dd
        i = 0
        self.date_partition = ''
        while self.date_partition == '':
            if re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}', df.select(first(f'partition_{i}')).collect()[0][0]):
                self.date_partition = f'partition_{i}'
            i += 1
            
        remove_list = ['CreationTime', 'Location', self.date_partition]
        columns = [column for column in df.columns if column not in remove_list]
        print(columns)
        
        df.groupBy(columns).agg(max("CreationTime").alias('CreationTime')).show()
        
        return df.groupBy(columns).agg(max("CreationTime").alias('CreationTime')).join(df, columns + ['CreationTime'], how = 'inner')
        

    def get_source_table(self):
        return None
        
    def get_bucket_name(self) -> str:
        """
        Get the name of the bucket where the table is located
        """
        self.bucket_name = self.get_source_last_partitions().select(first(f'Location')).collect()[0][0].split('/')[2]
        return self.bucket_name
        
    def save_parquet(self, df: SparkDataFrame, key: str) -> None:
        """
        target_uri: s3:// + self.bucket_name + key; key = path + file_name
        
        Example:
            key = '20-raw/git/{table_name}'
            
            target_uri = s3://{bucket_name}/20-raw/git/{table_name}/.../partition_n/{current_date}/supernovae.parquet
        """
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        
        key = key.split('/')
        key.insert(-1, today)
        key = '/'.join(key)
        
        self.get_bucket_name()
        
        target_uri = f"s3://{self.bucket_name}/{key}"
        
        df.write.mode('overwrite').parquet(target_uri) #add partitionBy(*list_of_partition_like_columns)
        
        return None