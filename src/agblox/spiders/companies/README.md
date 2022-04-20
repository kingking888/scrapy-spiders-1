# Spiders collection for obtaining companies data.

### How to obtain needed data from S3 bucket

With using this script: [s3_downloader.py](/src/agblox/spiders/companies/scripts/s3_downloader.py) and
it's main method ```obtain_data()```.

Example:
```
data = obtain_data(
    data_type="volumes",
    from_date="2021-11-15",
    to_date=2021-11-26)
```

| Parameter   |      Type     |                                                                                                                                                                                                                                                                                                         Options |
|----------   |:-------------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| data_type   |      str      | **One of**:<br>- tickers<br>- earnings<br> - dividends<br> -macro-data<br/> - volumes<br> - price-sector<br> - prices<br> - macro-yahoo<br> - companies<br> - us-fin-calc<br> - us-indu-calc<br> - us-indu-calc-key<br> - intrinio-weekly <br>- intrinio-monthly<br> - smb<br> - qual<br> - mom<br> - hml<br> - oecd |
| from_date   |      str      |                                                                                                                                                                                                                                                                                valid ISO date: ```2021-11-01``` |
| to_date     |      str      |                                                                                                                                                                                                                                                                                valid ISO date: ```2021-11-01``` |

### Spiders to data type reference
Each spider can produce different types of data.
See the table below to understand data type and spider's execution schedule.

| Spider name         |                              Data Type                              |  Schedule, UTC |
|----------           |:-------------------------------------------------------------------:|---------:|
| zacks_sp500         |                              - tickers                              | Fri 17:30, each week |
| yahoo_companies     |     - prices<br/>- volumes<br/>- price-sector<br/>-macro-yahoo      |   |
| intrinio_weekly     |                          -intrinio-weekly                           |   |
| intrinio_monthly    |                          -intrinio-monthly                          |    |
| intrinio_quarter    | -companies<br/>-us-fin-calc<br/>-us-indu-calc<br/>-us-indu-calc-key |    |
| fred_macro          |                             -macro-data                             |    |
| earnings_calendars  |                              -earnings                              |    |
| dividends_calendars |                             -dividends                              |    |
| global_data         |            -smb<br/>- qual<br/>- mom<br/>-hml<br/>-oecd             |    |
