# Pletora Utility Package

## Table of Contents

* [General Information](#general-information)
* [Technologies Used](#technologies-used)
* [The package is able to do](#the-package-is-able-to-do)
* [Creating the wheel file](#creating-the-wheel-file)
* [How to use the wheel file](#how-to-use-the-wheel-file)
* [Contributing](#contributing)
* [Contact](#contact)

## General Information

This repository contains the utility package for all [Pletora Data Solutions](https://github.com/Pletora-Data-Solutions) projects, which involves creating and manipulating tables and data lakes, using Amazon Web Services (AWS). 

In this repository you can find the python file with the utility package, in `pletora/pipeline.py`. Structuring the folders and files in the repository serves to generate a wheel file (executable pip package), which is needed to import the utility package into the AWS Glue job. Below is explained how to create and use the wheel file.

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

With the AWS Glue Job, we can manipulate the data lake in Amazon S3 and query tables in Amazon Athena, using Python/PySpark and SQL.

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
          >pipeline.py
~~~


2. Change directory in the command prompt and navigate to your project root directory where `setup.py` is placed. Execute `python setup.py bdist_wheel`. A file with `.whl` extension, named `pipeline-1.0-py3-none-any.whl`, was created in an auto created sub-directory under the root, named `dist`.

## How to use the wheel file

1. Create a Python file, named `import-pipeline.py`, to be used as a script for the AWS Glue job, and add the following code to the file:
~~~
from pletora.pipeline import Pipeline
~~~

2. Upload the files `pipeline-1.0-py3-none-any.whl` and `import-pipeline.py` to Amazon S3 Bucket. In our case, the uploaded file path is `s3://pletora-supernovae/scripts/libs/`.

3. On the AWS Glue console, in the `Job details` (Advanced properties) of the Job of interest, specify the path to the `.whl` file, i.e. `s3://pletora-supernovae/scripts/libs/pipeline-1.0-py3-none-any.whl`, in the `Python library path` box. In the `Script` of the Job, we can do for example:
~~~
from pletora.pipeline import Pipeline
pl = Pipeline(source_database, source_table, target_database, target_table, spark)
bucket_name = pl.get_bucket_name()
print(bucket_name)
~~~

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
    <td align="center"> <b> Lucas Corbanez </b> (Coordinator)</td>
    <td>
      <a href="https://github.com/Corbanez97" target="_blank"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" target="_blank"></a> 
      <a href="https://www.linkedin.com/in/lucas-corbanez/" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
      <a href = "mailto:lucascorbanez@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
      </td>
  </tr>
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