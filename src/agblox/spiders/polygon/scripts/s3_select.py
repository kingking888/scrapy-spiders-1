"""Module for selecting data from S3 objects."""

import logging

from agblox.settings import S3_BUCKET
import boto3


log = logging.getLogger(__name__)


def s3_select(ticker: str) -> str:
    """Select daily data for given ticker symbol from S3 file."""
    log.info(
        f"Data will be taken from to the S3 bucket {S3_BUCKET}",
    )
    client = boto3.client("s3")
    bucket = S3_BUCKET
    key = f"polygonator/{ticker}_stocks_daily_bars.csv.gz"
    expression_type = "SQL"
    expression = """SELECT * FROM s3object s"""
    input_serialization = {"CSV": {"FileHeaderInfo": "USE"}, "CompressionType": "GZIP"}
    output_serialization = {"JSON": {}}
    response = client.select_object_content(
        Bucket=bucket,
        Key=key,
        ExpressionType=expression_type,
        Expression=expression,
        InputSerialization=input_serialization,
        OutputSerialization=output_serialization,
    )
    for event in response["Payload"]:
        if "Records" in event:
            return event["Records"]["Payload"].decode("utf-8")
        elif "Stats" in event:
            return event["Stats"]


if __name__ == "__main__":
    s3_select("SNDL")
