"""Module for obtaining data from S3 bucket."""

# Requires: boto3, pytz
#
# Module usage
#
# 1. Import this module
# 2. Provide folloving environment variables to your script:
#      AWS_ACCESS_KEY_ID and
#      AWS_SECRET_ACCESS_KEY
# 3. Use the method obtain_data() for download needed datasets with parameters:
#      data_type (required) (- TYPE: FILE_EXAMPLE):
#         - tickers (tickers_2022-01-20T17:11:44.316386.json)
#         - earnings (earnings_ca_2021-11-22T18:28:31.273664.json)
#         - dividends (dividends_ca_2021-11-22T18:35:46.734158.json)
#         - volumes (volume_2021-11-23T18:51:09.946491.json)
#         - price-sector (price_sector_2022-01-20T22:42:56.659927.json)
#         - price ({TICKER}_2021-11-23T18:51:08.245860.json)
#         - macro-yahoo (macro_yahoo_2021-11-23T18:51:10.744072.json)
#         - macro-data (macro_data_2021-11-24T15:45:39.130305.json)
#         - intrinio-weekly ({TICKER}_2021-11-24T22:42:56.999382.json)
#         - intrinio-monthly ({TICKER}_2021-11-24T22:56:41.690313.json)
#         - companies (companies_2022-01-31T13:33:36.720123.gz)
#         - us-fin-calc (us-fin-calc_2022-01-31T13:33:22.674932.gz)
#         - us-indu-calc (companies_2022-01-31T13:33:36.720123.gz)
#         - smb (smb_2022-01-20T21_02_22.897816.xls.gz)
#         - qual (qual_2022-01-20T21_02_25.256029.xls.gz)
#         - mom (mom_2022-01-20T21_02_27.536195.xls.gz)
#         - hml (hml_2022-01-20T21_02_29.791849.xls.gz)
#         - oecd (oecd_2022-01-20T21_07_13.008637.xls.gz)
#      from_date (optional): YYYY-MM-DD
#      to_date (optional): YYYY-MM-DD

import datetime
from datetime import timedelta
import logging
import os
from pathlib import Path
import re
import sys
from timeit import default_timer as timer

from agblox.settings import S3_BUCKET
import boto3
from botocore.exceptions import ClientError
import dateutil.parser as dparser
import pytz


logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


class S3ReadingBasicException(Exception):
    """Basic exception for current module."""

    pass


s3 = boto3.client("s3")
bucket = S3_BUCKET


def filter_contents(from_date: str, to_date: str, contents: list) -> list:
    """Filter S3 bucket contents by date range.

    Args:
        from_date: date string, e.g. 2021-11-01
        to_date: date string, e.g. 2021-11-10
        contents: objects parameters list requested from S3 bucket
    Returns:
        Filtered list by date range.
    """
    start_date = datetime.datetime(2020, 1, 1).replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC
    )  # will be used by deault
    stop_date = datetime.datetime.utcnow().replace(
        hour=23, minute=59, second=59, microsecond=999999, tzinfo=pytz.UTC
    )  # will be used by deault
    filtered = []

    if from_date:
        try:
            start_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
        except ValueError:
            log.error("You need provide a valid date strings, e.g.: 2021-11-10")

    if to_date:
        try:
            stop_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, microsecond=999999, tzinfo=pytz.UTC
            )
        except ValueError:
            log.error("You need provide a valid date strings, e.g.: 2021-11-10")

    for item in contents:
        if start_date < key_to_date(item["Key"]) < stop_date:
            filtered.append(item)
    return filtered


def key_to_date(s3_key: str) -> datetime.date:
    """Parse S3 file key for date and return date object.

    Args:
        s3_key: filekey on S3

    Raises:
        S3ReadingBasicException: Raises a basic exception for this module.

    Returns:
        Defined date object or Exception.
    """
    match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}(_|:)\d{2}(_|:)\d{2}.\d+", s3_key)
    match = process_filename(match.group(), reverse=True)
    if not match:
        raise S3ReadingBasicException("Can't find date in given filepath: %s" % s3_key)
    return dparser.parse(match).replace(tzinfo=pytz.UTC)


def s3_path_map(data_type: str) -> str:
    """Maps data type to available data path on S3 bucket.

    Args:
        data_type:
            - tickers
            - earnings
            - dividends
            - volumes
            - price-sector
            - prices
            - macro-yahoo
            - macro-data
            - intrinio-weekly
            - intrinio-monthly
            - companies
            - us-fin-calc
            - us-indu-calc
            - smb
            - qual
            - mom
            - hml
            - oecd

    Returns:
        Path string.
    """
    possible_paths = {
        "tickers": "companies-models-data/tickers/",
        # "findata": "companies-models-data/findata/",
        "earnings": "companies-models-data/earnings/",
        "dividends": "companies-models-data/dividends/",
        "volumes": "companies-models-data/volume/",
        "price-sector": "companies-models-data/price-sector/",
        "prices": "companies-models-data/price/",
        "macro-yahoo": "companies-models-data/macro-yahoo/",
        "macro-data": "companies-models-data/macro-data/",
        "intrinio-weekly": "companies-models-data/intrinio-weekly/",
        "intrinio-monthly": "companies-models-data/intrinio-monthly/",
        "companies": "companies-models-data/companies/",
        "us-fin-calc": "companies-models-data/us-fin-calc/",
        "us-indu-calc": "companies-models-data/us-indu-calc/",
        "smb": "companies-models-data/smb/",
        "qual": "companies-models-data/qual/",
        "mom": "companies-models-data/mom/",
        "hml": "companies-models-data/hml/",
        "oecd": "companies-models-data/oecd/",
    }
    return possible_paths[data_type]


def process_filename(name: str, reverse: bool = False) -> str:
    """Replace spec chars in filename.

    Used for Windows hosts only.

    Args:
        name: Filename
        reverse: substitute backwards "_" -> ":"
    Returns:
        Processed filename
    """
    new_name = re.sub("[_]", ":", name) if reverse else re.sub("[:]", "_", name)
    return new_name


def obtain_data(data_type: str, from_date: str = None, to_date: str = None) -> list:
    """Main method for filtering and downloading the data.

    Args:
        data_type:
            - tickers
            - earnings
            - dividends
            - volumes
            - price-sector
            - prices
            - macro-yahoo
            - macro-data
            - companies
            - us-fin-calc
            - us-indu-calc
            - intrinio-weekly
            - intrinio-monthly
            - smb
            - qual
            - mom
            - hml
            - oecd
        from_date: date string, e.g. 2021-11-01
        to_date: date string, e.g. 2021-11-10

    Raises:
        ClientError: A botocore client error when response returns 404.

    Returns:
        List of file paths for all downloaded objects.
    """
    data_path = Path().absolute() / "data"
    os.makedirs(data_path, exist_ok=True)

    params = {"Bucket": bucket, "Prefix": s3_path_map(data_type)}
    filenames = []
    response = s3.list_objects(**params)
    try:
        request_files = response["Contents"]
    except KeyError:
        log.warning("Can't find data for type: [%s]. Check the bucket [%s]." % (data_type, bucket))
        sys.exit(1)
    filtered = filter_contents(from_date, to_date, request_files)
    for file in filtered:
        filename = file["Key"].split("/")[-1]
        if sys.platform == "win32":  # filename compatibility with Windows hosts
            filename = process_filename(filename)
        storage_path = data_path / filename
        try:
            with open(storage_path, "wb") as f:
                s3.download_fileobj(bucket, file["Key"], f)
            log.info("Download complete for file: %s" % filename)
            filenames.append(storage_path)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                log.warning("The object does not exist.")
            else:
                raise
    return filenames


if __name__ == "__main__":
    start = timer()
    obtain_data("us-indu-calc", from_date="2022-01-01", to_date="2022-01-31")
    log.info(f"Execution time: {timedelta(seconds=timer() - start)}")
