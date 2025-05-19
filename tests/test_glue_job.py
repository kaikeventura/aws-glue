from unittest.mock import patch, MagicMock

import pytest
from pyspark.sql import SparkSession

import src.glue_job as glue_job


@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").appName("pytest").getOrCreate()


def test_transform_df_transforms(spark):
    df = spark.createDataFrame([
        {"xpto_id": "1", "name": "Alice"},
        {"xpto_id": "1", "name": "Alice"},
        {"xpto_id": "2", "name": "Bob"},
    ])
    result = glue_job.transform_dataframe(df)
    data = result.collect()
    assert len(data) == 3
    assert set(row["id"] for row in data) == {"1", "1", "2"}
    assert all("active" in row.asDict() for row in data)


def test_removes_duplicates_from_dataframe(spark):
    dataframe = spark.createDataFrame([
        {"xpto_id": "1", "name": "Alice"},
        {"xpto_id": "1", "name": "Alice"},
        {"xpto_id": "2", "name": "Bob"},
    ])
    result = glue_job.remove_duplicates(dataframe=dataframe)
    data = result.collect()
    assert len(data) == 2
    assert set(row["xpto_id"] for row in data) == {"1", "2"}


@patch("src.glue_job.boto3.resource")
def test_write_to_dynamodb_success(mock_boto3, spark):
    mock_table = MagicMock()
    mock_boto3.return_value.Table.return_value = mock_table

    row = {"id": "123", "nome": "Fulano"}
    glue_job.write_to_dynamodb(row)

    mock_boto3.assert_called_once()
    mock_table.put_item.assert_called_once_with(Item=row)


@patch("src.glue_job.write_to_dynamodb", side_effect=Exception("Dynamo failure"))
def test_write_batch_to_dynamodb_error(mock_boto3, spark):
    df = spark.createDataFrame([
        {"xpto_id": "123", "name": "Fulano"},
    ])

    with pytest.raises(Exception, match="Dynamo failure"):
        glue_job.write_batch_to_dynamodb(df)


def test_write_batch_to_dynamodb_empty_df(spark):
    df = spark.createDataFrame([], "xpto_id STRING, nome STRING")
    glue_job.write_batch_to_dynamodb(df)
