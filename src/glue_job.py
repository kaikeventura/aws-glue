import sys
import boto3
from pyspark.sql import DataFrame

from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


def write_to_dynamodb(row_dict:dict[str,str], table_name:str="table_dynamodb", region:str="us-east-1"):
    try:
        dynamodb = boto3.resource("dynamodb", region_name=region)
        table = dynamodb.Table(table_name)
        table.put_item(Item=row_dict)
    except Exception as e:
        print(f"Error when trying insert data on DynamoDB: {e}")
        raise


def write_batch_to_dynamodb(dataframe: DataFrame):
    if dataframe.count() == 0:
        print("DataFrame is empty")
        return

    dataframe = remove_duplicates(dataframe)
    transformed_dataframe = transform_dataframe(dataframe)

    transformed_dataframe.foreach(lambda row: write_to_dynamodb(row.asDict()))


def remove_duplicates(dataframe: DataFrame):
    return dataframe.dropDuplicates(["xpto_id"])


def transform_dataframe(dataframe: DataFrame):
    return dataframe.rdd.map(lambda row: {
        "id": row["xpto_id"],
        "name": row["name"],
        "active": row.asDict(True).get("active", True)
    }).toDF()


def main():
    args = getResolvedOptions(sys.argv, ["JOB_NAME"])
    spark_context = SparkContext()
    glue_context = GlueContext(spark_context)
    job = Job(glue_context)
    job.init(args["JOB_NAME"], args)

    datasource = glue_context.create_dynamic_frame.from_catalog(
        database="s3_database",
        table_name="table_dynamodb"
    )

    dataframe = datasource.toDF()
    write_batch_to_dynamodb(dataframe=dataframe)

    job.commit()


if __name__ == "__main__":
    main()
