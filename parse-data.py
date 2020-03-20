#!/usr/bin/env python

import argparse
import csv
import os
import sys

from parsers import *


class Source(object):
    def __init__(self, name, filename, parser):
        self.name = name
        self.filename = filename
        self.parser = parser


SOURCES = [
    Source("covidtracker", "covidtracker-daily.csv", covid_parser),
    Source("csse",  "csse-confirmed.csv", csse_parser_confirmed),
    Source("csse", "csse-deaths.csv", csse_parser_deaths),
    Source("owid",  "owid-full_data.csv", owid_parser),
]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datadir', default='.', type=str, nargs='?')
    args = parser.parse_args()
    return args


def read_csv(args, source):
    filepath = os.path.join(args.datadir, source.filename)
    csvfile = open(filepath)
    return csv.DictReader(csvfile)


def find_max_date(master_map):
    max_date = dt.date.today() - dt.timedelta(1000)
    for v in master_map.values():
        for date in v.keys():
            max_date = max(date, max_date)
    return max_date


def main():
    args = get_args()
    master_map = {}
    for source in SOURCES:
        csv_list = read_csv(args, source)
        source.parser(csv_list, master_map)

    # Modify after this to process data as you wish or return

    max_date = find_max_date(master_map)
    three_weeks_ago = max_date - dt.timedelta(days=21)
    print(three_weeks_ago)

    for k, v in master_map.items():
        print(f'{k} total_cases owid ', end='')
        curr_day = three_weeks_ago
        while curr_day <= max_date:
            print(f"{v.get(curr_day, {}).get('owid', {}).get('total_cases', 0)} ", end='')
            curr_day = curr_day + dt.timedelta(days=1)
        print('')

    for k, v in master_map.items():
        print(f'{k} total_cases csse ', end='')
        curr_day = three_weeks_ago
        while curr_day <= max_date:
            print(f"{v.get(curr_day, {}).get('csse', {}).get('total_cases', 0)} ", end='')
            curr_day = curr_day + dt.timedelta(days=1)
        print('')

    for k, v in master_map.items():
        print(f'{k} total_cases covid ', end='')
        curr_day = three_weeks_ago
        while curr_day <= max_date:
            print(f"{v.get(curr_day, {}).get('covid', {}).get('total_cases', 0)} ", end='')
            curr_day = curr_day + dt.timedelta(days=1)
        print('')


if __name__ == '__main__':
    main()
