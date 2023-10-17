# AEMET
Extracting data from AEMET API and saving it in parquet files for easier loading in data platforms such as BigQuery.

The aim of this project is to extract the weather data from AEMET through their API and load it in a BigQuery dataset in order to later transform it via dbt.

This will allow anyone to check historical data such as temperature (min, max, average), rain, wind, etc. for several purposes (such as comparing news to actual data).

Next steps will include a daily update of the data.