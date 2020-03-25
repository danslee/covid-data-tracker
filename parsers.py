#!/usr/bin/env python

""" Parsers parse arrays of maps (presumably read in from csv files) into standard format

Master Dictionary

regions are tuples (country, [subdivision,] [microdivion])
datetime.date only days, no normalization of dates is attempted
type is a cross product of [total_, new_, rate_, weighted_rate_] and [cases, deaths]
for example:
    - total_cases
    - new_cases
    - rate_cases : ratio of new_cases / total_cases of day before
    - weighted_rate_cases : exponential smoothed rate_cases with smoothing factor SMOOTHING_FACTOR

{ source:
    { region:
        { type :
            { date: val
            }
        }
    }
}

"""

from collections import defaultdict
import datetime as dt
import region_normalize as rn
import re

SMOOTHING_FACTOR = 0.3
RATE_CUTOFF = 100
ONE_DAY = dt.timedelta(days=1)


def build_time_series():
    return defaultdict(int)


def build_region_dict():
    return defaultdict(build_time_series)


def build_source_dict():
    return defaultdict(build_region_dict)


def build_master_dict():
    return defaultdict(build_source_dict)


def add_raw_data_point(name, region, datatype, date, val, out_map):
    if not val:
        return
    out_map[name][region][datatype][date] = float(val)


def fill_gaps(time_series):
    dates = sorted(time_series.keys())
    if not len(dates):
        return
    start, end = dates[0], dates[-1]
    val = time_series[start]
    day = start
    while day <= end:
        if not time_series[day]:
            time_series[day] = val
        val = time_series[day]
        day += ONE_DAY


def fill_gaps_for_source(source_map, key):
    for region_data in source_map.values():
        fill_gaps(region_data[key])


def calc_deltas_for_time_series(time_series, delta_time_series):
    dates = sorted(time_series.keys())
    if not len(dates):
        return
    start, end = dates[0], dates[-1]
    delta_time_series[start] = time_series[start]
    day = start + ONE_DAY
    while day <= end:
        delta = time_series[day] - time_series[day - ONE_DAY]
        delta_time_series[day] = delta
        day += ONE_DAY


def calc_deltas(source_map, key, delta_key):
    for region_data in source_map.values():
        calc_deltas_for_time_series(region_data[key], region_data[delta_key])


def add_to_aggregation(source_ts, sum_ts):
    if not len(source_ts):
        return
    for date, value in source_ts.items():
        sum_ts[date] += value


def add_usa_aggregation(source_dict, key):
    usa_dict = source_dict[("United States of America",)]
    for region, region_data in source_dict.items():
        if not rn.is_us_state(region):
            continue
        add_to_aggregation(region_data[key], usa_dict[key])


def calc_rates_for_time_series(total_ts, delta_ts, rate_ts):
    if not len(total_ts):
        return
    day = sorted(total_ts.keys())[0] + ONE_DAY
    while day in delta_ts:
        rate = 0.0
        if total_ts[day - ONE_DAY] > RATE_CUTOFF:
            rate = 1.0 + float(delta_ts[day]) / total_ts[day - ONE_DAY]
            rate_ts[day] = rate
        day += ONE_DAY


def calc_rates(source_map, total_key, delta_key, rate_key):
    for region_data in source_map.values():
        if rate_key not in region_data:
            region_data[rate_key]
        calc_rates_for_time_series(region_data[total_key],
                                   region_data[delta_key],
                                   region_data[rate_key])


def calc_weighted_rates_for_time_series(rate_ts, weighted_rate_ts):
    if not len(rate_ts):
        print("BAD VALUES" + str(rate_ts) + str(weighted_rate_ts))
        return
    day = sorted(rate_ts.keys())[0]
    last_weighted_rate = rate_ts[day]
    while day in rate_ts:
        old_weight = (1.0 - SMOOTHING_FACTOR) * last_weighted_rate
        last_weighted_rate = (SMOOTHING_FACTOR * rate_ts[day]) + old_weight
        weighted_rate_ts[day] = last_weighted_rate
        print(weighted_rate_ts[day])
        day += ONE_DAY


def calc_weighted_rates(source_map, rate_key, weighted_rate_key):
    for region_data in source_map.values():
        if weighted_rate_key not in region_data:
            region_data[weighted_rate_key]
        calc_weighted_rates_for_time_series(region_data[rate_key], region_data[weighted_rate_key])


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
    add_raw_data_point('covid', region, 'total_cases', date, zero_missing(line, 'positive'),
                       out_map)
    add_raw_data_point('covid', region, 'total_deaths', date, zero_missing(line, 'death'), out_map)


def covid_parser(lines, out_map):
    for line in lines:
        print(line)
        state = line["state"]
        region = rn.normalize("USA", state)
        date = covid_str2date(line["date"])
        add_covid_data(region, date, line, out_map)

    covid_map = out_map["covid"]

    fill_gaps_for_source(covid_map, "total_cases")
    calc_deltas(covid_map, "total_cases", "new_cases")
    fill_gaps_for_source(covid_map, "total_deaths")
    calc_deltas(covid_map, "total_deaths", "new_deaths")

    add_usa_aggregation(covid_map, "total_cases")
    add_usa_aggregation(covid_map, "new_cases")
    add_usa_aggregation(covid_map, "total_deaths")
    add_usa_aggregation(covid_map, "new_cases")

    calc_rates(covid_map, "total_cases", "new_cases", "rate_cases")
    calc_weighted_rates(covid_map, "rate_cases", "weighted_rate_cases")
    calc_rates(covid_map, "total_deaths", "new_deaths", "rate_deaths")
    calc_weighted_rates(covid_map, "rate_deaths", "weighted_rate_deaths")


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
                add_raw_data_point('csse', region, datatype, date, val, out_map)


def csse_parser_confirmed(lines, out_map):
    csse_parser(lines, out_map, "total_cases")
    csse_map = out_map["csse"]

    fill_gaps_for_source(csse_map, "total_cases")
    calc_deltas(csse_map, "total_cases", "new_cases")

    add_usa_aggregation(csse_map, "total_cases")
    add_usa_aggregation(csse_map, "new_cases")

    calc_rates(csse_map, "total_cases", "new_cases", "rate_cases")
    calc_weighted_rates(csse_map, "rate_cases", "weighted_rate_cases")

    return


def csse_parser_deaths(lines, out_map):
    csse_parser(lines, out_map, "total_deaths")
    csse_map = out_map["csse"]

    fill_gaps_for_source(csse_map, "total_deaths")
    calc_deltas(csse_map, "total_deaths", "new_deaths")

    add_usa_aggregation(csse_map, "total_deaths")
    add_usa_aggregation(csse_map, "new_deaths")

    calc_rates(csse_map, "total_deaths", "new_deaths", "rate_deaths")
    calc_weighted_rates(csse_map, "rate_deaths", "weighted_rate_deaths")
    return


def owid_str2date(datestr):
    year, month, day = datestr.split("-")
    return dt.date(int(year), int(month), int(day))


def add_owid_data(region, date, line, out_map):
    add_raw_data_point("owid", region, "new_cases", date, zero_missing(line, "new_cases"), out_map)
    add_raw_data_point("owid", region, "total_cases", date, zero_missing(line, "total_cases"),
                       out_map)
    add_raw_data_point("owid", region, "new_deaths", date, zero_missing(line, "new_deaths"),
                       out_map)
    add_raw_data_point("owid", region, "total_deaths", date, zero_missing(line, "total_deaths"),
                       out_map)


def owid_parser(lines, out_map):
    for line in lines:
        region = rn.normalize(line["location"])
        date = owid_str2date(line["date"])
        add_owid_data(region, date, line, out_map)

    calc_rates(out_map["owid"], "total_cases", "new_cases", "rate_cases")
    calc_weighted_rates(out_map["owid"], "rate_cases", "weighted_rate_cases")
    calc_rates(out_map["owid"], "total_deaths", "new_deaths", "rate_deaths")
    calc_weighted_rates(out_map["owid"], "rate_deaths", "weighted_rate_deaths")


def main():
    # run_tests TBD
    pass


if __name__ == '__main__':
    main()
