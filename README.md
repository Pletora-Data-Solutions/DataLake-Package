# Pletora Utility Package

## Table of Contents

* [General Information](#general-information)
* [Technologies Used](#technologies-used)
* [The package is able to do](#the-package-is-able-to-do)
* [Creating the wheel file](#creating-the-wheel-file)
* [How to use the wheel file](#how-to-use-the-wheel-file)
* [Recommended storage structure](#recommended-storage-structure)
* [Contributing](#contributing)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

## General Information

This repository contains the utility package for all [Pletora Data Solutions](https://github.com/Pletora-Data-Solutions) projects, which involves creating and manipulating tables and data lakes, using Amazon Web Services (AWS). 

In this repository you can find the python file with the utility package, in `pletora/node.py`. Structuring the folders and files in the repository serves to generate a wheel file (executable pip package), which is needed to import the utility package into the AWS Glue Job. 

Below is explained how to create and use the wheel file as well as other features of the project.

## Technologies Used

* [Amazon Web Services (AWS)](https://aws.amazon.com/)
  * [AWS Glue 3.0](https://aws.amazon.com/glue/?nc1=h_ls)
    * [Job](https://docs.aws.amazon.com/glue/latest/dg/add-job.html)
    * [Crawler](https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html)
  * [Amazon S3](https://aws.amazon.com/pt/s3/)
  * [Amazon Athena](https://aws.amazon.com/athena/?nc1=h_ls)
* [Python 3](https://www.python.org/)
    * [PySpark - Spark 3.1](https://spark.apache.org/docs/latest/api/python/)
* [SQL](https://pt.wikipedia.org/wiki/SQL)

The utility package is initially developed using AWS Glue Jobs as the development environment. Once it is ready, the package is used to develop other Jobs and facilitate the development of the data pipeline.

A Job is the primary tool used to load and manipulate data in Amazon S3 or query tables with Amazon Athena. Jobs are created using Python/PySpark and SQL, while Amazon S3 serves as the storage for the data lake. AWS Glue Crawler is used to create the tables that are queried by Amazon Athena.

The data in the data lake can be utilized to train machine learning models, which can then be deployed using Amazon SageMaker. Additionally, Amazon Redshift can be used to create a data warehouse that stores the data in a structured format, enabling the creation of data visualization dashboards.

## The package is able to do

* SQL queries in Amazon S3, with Amazon Athena.
* Create a dataframe for SQL queries.
* Get a list of Amazon S3 URIs for the most recent folders partitions.
* Get the name of the bucket where the table is located.
* Save a dataframe as a Parquet file.

## Creating the wheel file

1. Clone this repository on your local machine. Below is the important structure to generate the wheel file. The other files aren't necessary, but they don't cause any problems.
~~~
>/Glue-DataLake-Utility-Package/
      >setup.py 
      >__init__.py  
      >/pletora/ 
          >__init__.py 
          >node.py
~~~


2. Change directory in the command prompt and navigate to your project root directory where `setup.py` is placed. Execute `python setup.py bdist_wheel`. A file with `.whl` extension, named `node-1.0-py3-none-any.whl`, was created in an auto created sub-directory under the root, named `dist`.

## How to use the wheel file

1. Create a Python file, named `import-node.py`, to be used as a script for the AWS Glue job, and add the following code to the file:
~~~
from pletora.node import Node
~~~

2. Upload the files `node-1.0-py3-none-any.whl` and `import-node.py` to Amazon S3 Bucket. In our case, the uploaded file path is `s3://pletora-supernovae/scripts/libs/`.

3. On the AWS Glue console, in the `Job details` (Advanced properties) of the Job of interest, specify the path to the `.whl` file, i.e. `s3://pletora-supernovae/scripts/libs/node-1.0-py3-none-any.whl`, in the `Python library path` box. In the `Script` of the Job, we can do for example:
~~~
from pletora.node import Node
nd = Node(source_database, source_table, target_database, target_table, spark)
bucket_name = nd.get_bucket_name()
print(bucket_name)
~~~

## Recommended storage structure

The utility package has been designed to operate within a specific folder structure that facilitates the storage and management of data. Our data is stored in an Amazon S3 bucket, which serves as the foundation for our data lake. In order to ensure that our data is dependable and of the highest quality, it is divided into four layers: `10-landing`, `20-bronze`, `30-silver` and `40-gold`. The numbers at the front of each folder name maintain the correct order of the folders. In addition to these layers, we also have `logs`, `scripts` and `temp` folders.

Through this multi-layered approach, we have created an environment that enables users with varying levels of technical expertise to easily access and analyze the data in our data lake.

#### `10-landing`

It is the destination for new data as it arrives in the data lake. Within this layer, we have a file structure that shows the origin of the data, in addition to a folder that indicates the date of its upload. In this layer, files are kept in their original format. For example, we have the S3 URI:
~~~
s3://bucket-name/10-landing/partition_1/partition_2/ ... /partition_n/file
~~~
The partition_1 through partition_n-1 sections indicate the characteristics of the data source, and partition_n specifies the upload date in the format YYYY-MM-DD.

#### `20-bronze`

In this layer, data is transformed into Parquet format and in some cases it is necessary to make some changes to mitigate issues. We chose the Parquet format because it is a columnar storage format that provides efficient compression and encoding schemes. This makes it easier and faster to query the data later using Amazon Athena. The folder structure is the same as the previous layer, with the difference that the filename is automatically generated by PySpark. For example: 
~~~
s3://bucket-name/20-bronze/partition_1/partition_2/ ... /partition_n/autogenerated_name.parquet.
~~~

#### `30-silver`

For this layer, we reorganize the previous layer's data into tables. We only use the most up-to-date files. From this, we built general tables about the supernovae. For example:
~~~
s3://bucket-name/30-silver/table_name/autogenerated_name.parquet
~~~

#### `40-gold`

At this stage, it's the same tables and folder structure as the previous layer. However, the data in this layer has been processed and validated, and users can be confident in its quality and accuracy.

#### `logs`

Log files are software-generated files containing information about the operations, activities, and usage patterns of our data lake.

#### `scripts`

In this folder, the wheel file is located.

#### `temp`

Temporary files and folders that expire after a specified interval.

## Contributing 

Contributions are greatly appreciated!

1. Fork the project.
2. Create your feature branch: `git checkout -b feature/AmazingFeature`.
3. Commit your changes: `git commit -m 'Add some amazing stuff'`.
4. Push to the branch: `git push origin feature/AmazingFeature`.
5. Create a new Pull Request.

Issues and feature requests are welcome!

## Contact

Feel free to send contributions, reviews, questions and/or suggestions for each of the project participants:

<div  align="center"> 
<table>
  <tr>
    <td align="center"> <b> Adriano Junior Gouveia Gonçalves </b> </td>
    <td>
      <a href="https://github.com/DrAdriano" target="_blank"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" target="_blank"></a> 
      <a href="https://www.linkedin.com/in/sradriano/" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
      <a href = "mailto:sradriano@uel.br"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
    </td>
  </tr>
  <tr>
    <td align="center"> <b> Douglas Sanini </b> </td>
    <td>
      <a href="https://github.com/douglas-sanini" target="_blank"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" target="_blank"></a> 
      <a href="https://www.linkedin.com/in/douglas-sanini/" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
      <a href = "mailto:sanini.douglas@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
    </td>
  </tr>
</table>
</div>

## Acknowledgements

I would like to express my gratitude to [Lucas Corbanez](https://github.com/Corbanez97), who provided many tips on how this project could be developed.
