# COVID data tracker collector

The tools in this directory do a few things
  - fetch raw data from several sources
    - [The COVID Tracking Project](https://covidtracking.com/)
      - [daily data url](http://covidtracking.com/api/states/daily.csv)
    - [Johns Hopkins CSSE COVID-19](ttps://github.com/CSSEGISandData/COVID-19)
      - [confirmed count url](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv)
      - [death count url](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv)
    - [Our World in Data Coronavirus](https://ourworldindata.org/coronavirus)
      - It looks like OWID has switched from using the World Health Organization (WHO) as their data source to
        using the European Center for Disease Control and Prevention (ECDC) as their source. 
      - [OLD full data url](https://covid.ourworldindata.org/data/full_data.csv)
      - [current full data url](https://covid.ourworldindata.org/data/ecdc/full_data.csv)
    - this data is stored locally as files.
  - parse the above data into a unified map of data and print said data in table format.
  - there are other data sources, but don't freely publish their data
    - [1Point3Acres](https://coronavirus.1point3acres.com/en)

This has only been tested on MacOS 10.15 with python 3.7.4.
And a plug here for pyenv and virtualenv for mac development.

## Download data get-covid-data.py

python get-covid-data.py -d data_dir

## Parse data parse-data.py

python parse-data.py -d data_dir

## Notes

Country names are from iso-3166, I know there's all kinds of thoughts and disputes about Taiwan etc. etc. There
are better times to talk about that stuff.

## Attribution

all-countries.csv is from [lukes/iso-3166 project](https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv)
which is shared via [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

## Gotchas

### If you run into SSL: CERTIFICATE_VERIFY_FAILED

https://stackoverflow.com/questions/35569042/ssl-certificate-verify-failed-with-python3

