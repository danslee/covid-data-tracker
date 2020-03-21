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
    print(f"{region} {date} {name} {datatype} {val}")
    if not val:
        val = 0
    if region not in out_map:
        out_map[region] = {}
    if date not in out_map[region]:
        out_map[region][date] = {}
    if name not in out_map[region][date]:
        out_map[region][date][name] = {}
    out_map[region][date][name][datatype] = val


def add_data_point_cascade(region, date, name, datatype, val, out_map):
    add_raw_data_point(region, date, name, datatype, val, out_map)


def fill_gaps(source, key, out_map):
    pass


def calc_deltas(source, key, delta_key, out_map):
    pass


def zero_missing(inmap, key):
    if key not in inmap:
        return 0
    val = inmap[key]
    if not val:
        return 0
    return val


def noop_parser(lines, out_map):
    pass


def covid_str2date(datestr):
    year = int(datestr[:4])
    month = int(datestr[4:6])
    day = int(datestr[6:8])
    return dt.date(year, month, day)


def add_covid_data(region, date, line, out_map):
    add_raw_data_point(region, date, 'covid', 'total_cases', zero_missing(line, 'positive'), out_map)
    add_raw_data_point(region, date, 'covid', 'total_deaths', zero_missing(line, 'death'), out_map)


def covid_parser(lines, out_map):
    for line in lines:
        print(line)
        state = line["state"]
        region = rn.normalize("USA", state)
        date = covid_str2date(line["date"])
        add_covid_data(region, date, line, out_map)


def csse_str2date(datestr):
    month, day, year = datestr.split('/')
    return dt.date(2000 + int(year), int(month), int(day))


def csse_parser(lines, out_map, datatype):
    for line in lines:
        subdivision = line["Province/State"]
        country = line["Country/Region"]
        region = rn.normalize(country, subdivision)
        for item in line:
            if re.match(r"\d\d?/\d\d?/\d\d", item):
                val = line[item]
                date = csse_str2date(item)
                add_data_point_cascade(region, date, "csse", datatype, val, out_map)


def csse_parser_confirmed(lines, out_map):
    csse_parser(lines, out_map, "total_cases")
    fill_gaps("csse", "total_cases", out_map)
    calc_deltas("csse", "total_cases", "new_cases", out_map)
    return


def csse_parser_deaths(lines, out_map):
    csse_parser(lines, out_map, "total_deaths")
    fill_gaps("csse", "total_deaths", out_map)
    calc_deltas("csse", "total_deaths", "new_deaths", out_map)
    return


def owid_str2date(datestr):
    year, month, day = datestr.split("-")
    return dt.date(int(year), int(month), int(day))


def add_owid_data(region, date, line, out_map):
    add_raw_data_point(region, date, 'owid', 'new_cases', zero_missing(line, 'new_cases'), out_map)
    add_raw_data_point(region, date, 'owid', 'total_cases', zero_missing(line, 'total_cases'), out_map)
    add_raw_data_point(region, date, 'owid', 'new_deaths', zero_missing(line, 'new_deaths'), out_map)
    add_raw_data_point(region, date, 'owid', 'total_deaths', zero_missing(line, 'total_deaths'), out_map)


def owid_parser(lines, out_map):
    for line in lines:
        region = rn.normalize(line["location"])
        date = owid_str2date(line["date"])
        add_owid_data(region, date, line, out_map)


def main():
    #run_tests TBD
    pass


if __name__ == '__main__':
    main()
