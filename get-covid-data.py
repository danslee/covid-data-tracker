#!/usr/bin/env python

import argparse
import os
import sys
import urllib.request

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


class Source(object):
    def __init__(self, name, url, filename):
        self.name = name
        self.url = url
        self.filename = filename


SOURCES = [
    Source("owid", "https://covid.ourworldindata.org/data/full_data.csv", "owid-full_data.csv"),
    #Source("covidtracker", "http://covidtracking.com/api/states/daily.csv", "covidtracker-daily.csv"),
    Source("csse", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv", "csse-confirmed.csv"),
    Source("csse", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv", "csse-deaths.csv"),
    ]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datadir', default='.', type=str, nargs='?')
    args = parser.parse_args()
    return args


def get_source(args, source):
    print(f"reading '{source.name}' from '{source.url}' into '{source.filename}'")
    outfile = os.path.join(args.datadir, source.filename)
    urllib.request.urlretrieve(source.url, outfile)


def main():
    args = get_args()
    for source in SOURCES:
        get_source(args, source)


if __name__ == '__main__':
    main()
