# COVID data tracker collector

The tools in this directory do a few things
  - fetch raw data from several sources
    - https://covidtracking.com/
      - https://covidtracking.com/api/states/daily : json
    - https://github.com/CSSEGISandData/COVID-19
      - https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv
      - https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv
    - https://ourworldindata.org/coronavirus
      - https://covid.ourworldindata.org/data/full_data.csv : csv
    - in default mode, this data is stored locally as files.
  - parse the above data into a unified map of data and print said data in table format.

This has only been tested on MacOS 10.15 with python 3.7.4.

## Download data get-covid-data.py


## Parse data parse-covid-data.py


## Attribution

all-countries.csv is from [lukes/iso-3166](https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv)
which is shared via [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

## Gotchas

### If you run into SSL: CERTIFICATE_VERIFY_FAILED

https://stackoverflow.com/questions/35569042/ssl-certificate-verify-failed-with-python3

