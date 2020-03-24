#!/usr/bin/env python

import argparse
import csv
import datetime as dt
import parsers
import os


class Source(object):
    def __init__(self, name, filename, parser):
        self.name = name
        self.filename = filename
        self.parser = parser


SOURCES = [
    Source("covidtracker", "covidtracker-daily.csv", parsers.covid_parser),
    Source("csse", "csse-confirmed.csv", parsers.csse_parser_confirmed),
    Source("csse", "csse-deaths.csv", parsers.csse_parser_deaths),
    Source("owid", "owid-full_data.csv", parsers.owid_parser),
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
    for source in master_map.values():
        for region in source.values():
            for valtype in region.values():
                for date in valtype.keys():
                    max_date = max(date, max_date)
    return max_date


def print_time_series(start_date, header, time_series):
    def int_or_float(header, value):
        if "rate_" in header:
            return f"{value:.3f}"
        return f"{value:.0f}"
    if not len(time_series.keys()):
        return
    min_date = sorted(time_series.keys())[0]
    print(header, end=" ")
    curr_day = max(start_date, min_date)
    while curr_day in time_series:
        print(f" {int_or_float(header, time_series[curr_day])}", end="")
        curr_day = curr_day + dt.timedelta(days=1)
    print("")


def print_region_data(start_date, header, region_data):
    for key, time_series in region_data.items():
        print_time_series(start_date, f"{header}:{key}", time_series)


def print_source_data(start_date, name, source_data):
    for region, region_data in source_data.items():
        print_region_data(start_date, f"{name}:{region}", region_data)


def print_master_map(start_date, master_map):
    for name, source_data in master_map.items():
        print_source_data(start_date, name, source_data)


def main():
    args = get_args()
    master_map = parsers.build_master_dict()
    for source in SOURCES:
        csv_list = read_csv(args, source)
        source.parser(csv_list, master_map)

    # Modify after this to process data as you wish or return

    max_date = find_max_date(master_map)
    three_weeks_ago = max_date - dt.timedelta(days=21)
    print("ZZZ", three_weeks_ago)
    print_master_map(three_weeks_ago, master_map)


"""
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
"""

if __name__ == '__main__':
    main()
