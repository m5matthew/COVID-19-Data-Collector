'''
Statistical Machine Learning Lab at UCLA
This script collects COVID-19 hospital data by city.

Data Collected:
- 'Geographic Area Name'
- 'Total Population'
- 'Population per square meter (Population Density)'
- 'Population 65 Years and Over'
- 'Percent of Population that is 65 Years and Over'
- 'Percentage of people whose income in the past 12 months is below the poverty level'

Sources:
https://www.arcgis.com/home/item.html?id=1044bb19da8d4dbfb6a96eb1b4ebf629#overview
'''

import arcgis
from pathlib import Path


def main():
    # Query by state and by county
    url = "https://services7.arcgis.com/LXCny1HyhQCUSueu/arcgis/rest/services/Definitive_Healthcare_USA_Hospital_Beds/FeatureServer/0/query"
    data = arcgis.get_data(url)

    # Desired data columns
    # See documentation: https://services7.arcgis.com/LXCny1HyhQCUSueu/arcgis/rest/services/Definitive_Healthcare_USA_Hospital_Beds/FeatureServer/0
    desired_columns = {
        'HOSPITAL_NAME': 'Hospital Name',
        'HOSPITAL_TYPE': 'Hospital Type',
        'HQ_CITY': 'City',
        'COUNTY_NAME': 'County',
        'STATE_NAME': 'State',
        'NUM_LICENSED_BEDS': '# of Licensed Beds',
        'NUM_STAFFED_BEDS': '# of Staffed Beds',
        'NUM_ICU_BEDS': '# of ICU Beds',
        'ADULT_ICU_BEDS': '# of Adult ICU Beds',
        'PEDI_ICU_BEDS': '# of Pediatric ICU Beds',
        'BED_UTILIZATION': 'Bed Utilization Rate',
        'Potential_Increase_In_Bed_Capac': 'Potential Increase in Bed Capacity',
        'AVG_VENTILATOR_USAGE': 'Average Ventilator Usage'
    }

    df = arcgis.json_to_df(data, desired_columns)

    folder = 'hospital_beds'
    Path(folder).mkdir(exist_ok=True)
    df.to_csv(folder + '/hospitals.csv')


if __name__ == '__main__':
    main()
