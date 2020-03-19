#!/usr/bin/env python

""" Parsers parse arrays of maps (presumably read in from csv files) into standard format

Master Dictionary

{ region:                                 # regions are tuples (country, [subdivision,] [microdivion]) of len 1-3
    { date:                               # datetime.date only days, no normalization of dates is attempted
        { name:                           # name of source, csse, owid, covidtracker
            { 'new_cases':val,
              'new_deaths':val,
              'total_cases':val,
              'total_deaths':val,
            }
        }
    }
}

"""


import datetime as dt
import region_normalize as rn
import re


def add_raw_data_point(region, date, name, datatype, val, out_map):
    if not val:
        val = 0
    if region not in out_map:
        out_map[region] = {}
    if date not in out_map[region]:
        out_map[region][date] = {}
    if name not in out_map[region][date]:
        out_map[region][date][name] = {}
    out_map[region][date][name][datatype] = val


def add_data_point(region, date, name, datatype, val, out_map):
    add_raw_data_point(region, date, name, datatype, val, out_map)


def noop_parser(lines, out_map):
    pass

def owid_str2date(datestr):
    year, month, day = datestr.split("-")
    return dt.date(int(year), int(month), int(day))


def add_owid_data(region, date, line, out_map):
    add_raw_data_point(region, date, 'owid', 'new_cases', line.get('new_cases', 0), out_map)
    add_raw_data_point(region, date, 'owid', 'total_cases', line.get('total_cases', 0), out_map)
    add_raw_data_point(region, date, 'owid', 'new_deaths', line.get('new_deaths', 0), out_map)
    add_raw_data_point(region, date, 'owid', 'total_deaths', line.get('total_deaths', 0), out_map)


def owid_parser(lines, out_map):
    for line in lines:
        region = rn.normalize(line["location"])
        date = owid_str2date(line["date"])
        add_owid_data(region, date, line, out_map)


def csse_str2date(datestr):
    month, day, year = datestr.split('/')
    return dt.date(int(year), int(month), int(day))


def csse_parser(lines, out_map, datatype):
    local = {}
    for line in lines:
        subdivision = line["Province/State"]
        country = line["Country/Region"]
        region = rn.normalize(country, subdivision)
        for item in line:
            if re.match(r"\d\d?/\d\d?/\d\d", item):
                val = line[item]
                date = csse_str2date(item)
                add_data_point(region, date, "csse", datatype, val, out_map)


def csse_parser_confirmed(lines, out_map):
    return csse_parser(lines, out_map, "total_cases")


def csse_parser_deaths(lines, out_map):
    return csse_parser(lines, out_map, "total_deaths")


def main():
    #run_tests TBD
    pass


if __name__ == '__main__':
    main()
