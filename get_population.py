'''
Statistical Machine Learning Lab at UCLA
This script collects COVID-19 population data by state and by county.

Data Collected:
- 'Geographic Area Name'
- 'Total Population'
- 'Population per square meter (Population Density)'
- 'Population 65 Years and Over'
- 'Percent of Population that is 65 Years and Over'
- 'Percentage of people whose income in the past 12 months is below the poverty level'

Sources:
https://uscensus.maps.arcgis.com/home/item.html?id=44883cd255c14e6386199acb802e1dbd
'''

import requests
import pandas as pd
from pathlib import Path


def main():
    # Query by state and by county
    # Format documentation: https://developers.arcgis.com/rest/services-reference/query-feature-service-layer-.htm
    state = 0
    county = 1
    query = {
        'f': 'json',
        'outFields': '*',
        'returnGeometry': 'false',
        'where': '1=1'
    }
    state_url = f'https://services8.arcgis.com/DlJzJLOZpPXmMpWi/arcgis/rest/services/ACS_Percent_Households_Below_Poverty/FeatureServer/{state}/query'
    county_url = f'https://services8.arcgis.com/DlJzJLOZpPXmMpWi/arcgis/rest/services/ACS_Percent_Households_Below_Poverty/FeatureServer/{county}/query'
    s = requests.post(state_url, data=query)
    c = requests.post(county_url, data=query)
    state_data = s.json()
    county_data = c.json()

    # Desired data columns
    # Check https://services8.arcgis.com/DlJzJLOZpPXmMpWi/ArcGIS/rest/services/ACS_Percent_Households_Below_Poverty/FeatureServer/ for more index names
    state_desired_columns = {
        'NAME': 'Geographic Area Name',
        'B01001_001E': 'Total Population',
        'B01001_calc_PopDensity': 'Population per square meter (Population Density)',
        'Population_65_Years_and_Over': 'Population 65 Years and Over',
        'Percent_of_Population_that_is_6': 'Percent of Population that is 65 Years and Over',
        'DP03_0128PE': 'Percentage of people whose income in the past 12 months is below the poverty level'
    }
    county_desired_columns = {
        'NAME': 'Geographic Area Name',
        'State': 'State',
        'B01001_001E': 'Total Population',
        'B01001_calc_PopDensity': 'Population per square meter (Population Density)',
        'Population_65_Years_and_Over': 'Population 65 Years and Over',
        'Percent_of_Population_that_is_6': 'Percent of Population that is 65 Years and Over',
        'DP03_0128PE': 'Percentage of people whose income in the past 12 months is below the poverty level'
    }

    county_df = json_to_df(county_data, county_desired_columns.keys())
    state_df = json_to_df(state_data, state_desired_columns.keys())

    Path('population').mkdir(exist_ok=True)
    county_df.to_csv('population/counties.csv')
    state_df.to_csv('population/states.csv')


def json_to_df(json_data, desired_columns):
    headers = {}
    for x in json_data['fields']:
        headers[x['name']] = x['alias']
    data = [x['attributes'] for x in json_data['features']]
    df = pd.DataFrame(data, columns=headers)
    df = df[desired_columns]
    df
    df.rename(columns=headers, inplace=True)
    return df


if __name__ == '__main__':
    main()
