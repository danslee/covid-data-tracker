#!/usr/bin/env python

import argparse
import datetime as dt
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
    Source("covidtracker", "http://covidtracking.com/api/states/daily.csv", "covidtracker-daily.csv"),
    Source("csse", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv", "csse-confirmed.csv"),
    Source("csse", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv", "csse-deaths.csv"),
    Source("owid", "https://covid.ourworldindata.org/data/full_data.csv", "owid-full_data.csv"),
    ]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datadir', default='.', type=str, nargs='?', help="directory to store/read datafiles")
    parser.add_argument('-t', '--ttl_minutes', default='60', type=int, nargs='?', help="ttl for datafiles in minutes")
    args = parser.parse_args()
    return args


def check_ttl(outfile, ttl_seconds):
    if os.path.isfile(outfile):
        mtime = dt.datetime.utcfromtimestamp(os.path.getmtime(outfile))
        stale_time = dt.datetime.utcnow() - dt.timedelta(0, ttl_seconds)
        if mtime > stale_time:
            return True
    return False


def get_source(args, source):
    outfile = os.path.join(args.datadir, source.filename)
    if check_ttl(outfile, args.ttl_minutes * 60):
        print(f"skipping reading '{source.name}' from '{source.url}' into '{source.filename}' as file is still fresh " +
              f" within the ttl of {args.ttl_minutes} minutes.")
        return
    print(f"reading '{source.name}' from '{source.url}' into '{source.filename}'")
    req = urllib.request.Request(source.url, headers={'User-Agent': 'Mozilla/5.0'})
    with open(outfile, 'wb') as output_file:
        output_file.write(urllib.request.urlopen(req).read())


def main():
    args = get_args()
    for source in SOURCES:
        get_source(args, source)


if __name__ == '__main__':
    main()
