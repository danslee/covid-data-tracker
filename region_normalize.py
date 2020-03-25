#!/usr/bin/env python

import csv
import os
import sys

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

# Read in country list and build a map of names
COUNTRIES = {}
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
filepath = os.path.join(__location__, 'countries.csv')
csvfile = open(filepath)
countries = csv.DictReader(csvfile)
for country_dict in countries:
    name = country_dict['name']
    COUNTRIES[name] = country_dict
    first_name = name.split(",")[0]
    if first_name not in COUNTRIES:
        COUNTRIES[first_name] = country_dict
    first_name = name.split(" ")[0]
    if first_name not in COUNTRIES:
        COUNTRIES[first_name] = country_dict
    COUNTRIES["Cruise Ship"] = {"name": "Cruise Ship"}
    COUNTRIES["World"] = {"name": "World"}
    COUNTRIES["Vatican"] = {"name": "World"}

MISSING_COUNTRIES = ["Cruise Ship", "World", "Vatican"]

STATES = {'Alaska': 'AK', 'Alabama': 'AL', 'Arkansas': 'AR', 'American Samoa': 'AS',
          'Arizona': 'AZ', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT',
          'District of Columbia': 'DC', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
          'Guam': 'GU', 'Hawaii': 'HI', 'Iowa': 'IA', 'Idaho': 'ID', 'Illinois': 'IL',
          'Indiana': 'IN', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
          'Massachusetts': 'MA', 'Maryland': 'MD', 'Maine': 'ME', 'Michigan': 'MI',
          'Minnesota': 'MN', 'Missouri': 'MO', 'Northern Mariana Islands': 'MP',
          'Mississippi': 'MS', 'Montana': 'MT', 'National': 'NA', 'North Carolina': 'NC',
          'North Dakota': 'ND', 'Nebraska': 'NE', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
          'New Mexico': 'NM', 'Nevada': 'NV', 'New York': 'NY', 'Ohio': 'OH', 'Oklahoma': 'OK',
          'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI',
          'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
          'Utah': 'UT', 'Virginia': 'VA', 'Virgin Islands': 'VI', 'Vermont': 'VT',
          'Washington': 'WA', 'Wisconsin': 'WI', 'West Virginia': 'WV', 'Wyoming': 'WY'}

REV_STATES = res = dict((v, k) for k, v in STATES.items())

NORMALIZED_COUNTRIES = {
    "Cote d'Ivoire": "Côte d'Ivoire",
    "Czech Republic": "Czechia",
    "Gambia, The": "Gambia",
    "GB": "United Kingdom of Great Britain and Northern Ireland",
    "Great Britain": "United Kingdom of Great Britain and Northern Ireland",
    "Hong Kong China": "Hong Kong",
    "Iran": "Iran (Islamic Republic of)",
    "Korea, North": "Korea (Democratic People's Republic of)",
    "Korea, South": "Korea, Republic of",
    "Mainland China": "China",
    "North Korea": "Korea (Democratic People's Republic of)",
    "Democratic Republic of Congo": "Congo, Democratic Republic of the",
    "Republic of Congo": "Congo",
    "Republic of the Congo": "Congo",
    "Russia": "Russian Federation",
    "South Korea": "Korea, Republic of",
    "Taipei and environs": "Taiwan, Province of China",
    "Taiwan*": "Taiwan, Province of China",
    "The Bahamas": "Bahamas",
    "The Gambia": "Gambia",
    "UK": "United Kingdom of Great Britain and Northern Ireland",
    "UK": "United Kingdom",
    "US": "United States of America",
    "USA": "United States of America",
    "United Kingdom": "United Kingdom of Great Britain and Northern Ireland",
    "United States": "United States of America",
    "Vietnam": "Viet Nam",
    "Swaziland": "Kingdom of Eswatini",
    "Macedonia": "North Macedonia",
}


def is_us_state(region):
    """checks to see if the normalized region tuple is a state in the USA"""
    if len(region) != 2:
        return False
    if region[0] != "United States of America":
        return False
    if region[1] not in REV_STATES:
        return False
    return True


def normalize_country(country):
    global COUNTRIES, NORMALIZED_COUNTRIES
    if country in COUNTRIES:
        return COUNTRIES[country]["name"]
    if country in NORMALIZED_COUNTRIES:
        country = NORMALIZED_COUNTRIES[country]
    if country in COUNTRIES:
        return COUNTRIES[country]["name"]
    country = country + " NOT FOUND"
    return country


def normalize_subdivision(subdivision):
    if subdivision in STATES:
        return STATES[subdivision]
    return subdivision


def normalize(country, subdivision=None, microdivision=None):
    """ returns a list consisting of either a
        (country),
        (country, subdivision), or
        (country, subdivision, subsubdivision)
    """
    global COUNTRIES, STATES, NORMALIZED_COUNTRIES
    country = normalize_country(country)
    if not subdivision:
        return country,
    if subdivision == normalize_country(subdivision) and subdivision not in STATES:
        country = subdivision
        subdivision = microdivision
    if not subdivision:
        return country,
    subdivision = normalize_subdivision(subdivision)
    if not subdivision:
        return country,
    if not microdivision:
        return country, subdivision
    microdivision = normalize_subdivision(subdivision)
    if not microdivision:
        return country, subdivision
    return country, subdivision, microdivision


def main():
    print(all([
        normalize("China") == ("China",),
        normalize("Korea") == ("Korea, Republic of",),
        normalize("China", "Hong Kong") == ("Hong Kong",),
        normalize("US") == ("United States of America",),
        normalize("US", "California") == ("United States of America", "CA"),
        normalize("USA", "CA") == ("United States of America", "CA"),
        normalize("USA", "District of Columbia") == ("United States of America", "DC"),
    ]))


if __name__ == '__main__':
    main()
