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

import arcgis
from pathlib import Path


def main():
    # Query by state and by county
    state = 0
    county = 1
    state_url = f'https://services8.arcgis.com/DlJzJLOZpPXmMpWi/arcgis/rest/services/ACS_Percent_Households_Below_Poverty/FeatureServer/{state}/query'
    county_url = f'https://services8.arcgis.com/DlJzJLOZpPXmMpWi/arcgis/rest/services/ACS_Percent_Households_Below_Poverty/FeatureServer/{county}/query'
    state_data = arcgis.get_data(state_url)
    county_data = arcgis.get_data(county_url)

    # Desired data columns
    # Check https://services8.arcgis.com/DlJzJLOZpPXmMpWi/ArcGIS/rest/services/ACS_Percent_Households_Below_Poverty/FeatureServer/ for more index names
    total_population = 'B01001_001E'
    percent_people_below_poverty = 'DP03_0128PE'
    state_desired_columns = ['NAME', total_population, 'B01001_calc_PopDensity',
                             'Population_65_Years_and_Over', 'Percent_of_Population_that_is_6', percent_people_below_poverty]
    county_desired_columns = ['NAME', 'State', total_population, 'B01001_calc_PopDensity',
                              'Population_65_Years_and_Over', 'Percent_of_Population_that_is_6', percent_people_below_poverty]

    county_df = arcgis.json_to_df(county_data, county_desired_columns)
    state_df = arcgis.json_to_df(state_data, state_desired_columns)
    county_df = arcgis.rename_to_default_alias(county_df, county_data)
    state_df = arcgis.rename_to_default_alias(state_df, state_data)

    Path('population').mkdir(exist_ok=True)
    county_df.to_csv('population/counties.csv')
    state_df.to_csv('population/states.csv')


if __name__ == '__main__':
    main()
