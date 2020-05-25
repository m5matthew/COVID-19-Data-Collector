'''
Statistical Machine Learning Lab at UCLA
This script collects COVID-19 hospital data by city.

Data Collected:
- # Licensed Beds
- # Staffed Beds
- # ICU Beds
- # of ICU Beds
- # of Adult ICU Beds
- # of Pediatric ICU Beds
- Bed Utilization Rate
- Potential Increase in Bed Capacity
- Average Ventilator Usage

Sources:
Updated every Monday: https://www.arcgis.com/home/item.html?id=1044bb19da8d4dbfb6a96eb1b4ebf629#overview
'''

import arcgis
import pathlib
import pandas as pd


def group_by_sum(df, join_keys): return df.groupby(join_keys).sum()


def group_by_mean(df, join_keys): return df.groupby(join_keys).mean()


join_keys = ['COUNTY_NAME', 'STATE_NAME']
features = {
    'NUM_LICENSED_BEDS': {'csvfile': 'licensed_beds.csv', 'groupby': group_by_sum},
    'NUM_STAFFED_BEDS': {'csvfile': 'staffed_beds.csv', 'groupby': group_by_sum},
    'NUM_ICU_BEDS': {'csvfile': 'icu_beds.csv', 'groupby': group_by_sum},
    'ADULT_ICU_BEDS': {'csvfile': 'adult_icu_beds.csv', 'groupby': group_by_sum},
    'PEDI_ICU_BEDS': {'csvfile': 'pedi_icu_beds.csv', 'groupby': group_by_sum},
    'BED_UTILIZATION': {'csvfile': 'bed_utilization.csv', 'groupby': group_by_mean},
    'AVG_VENTILATOR_USAGE': {'csvfile': 'ventilator_usg.csv', 'groupby': group_by_mean}
}


def main():
    url = "https://services7.arcgis.com/LXCny1HyhQCUSueu/arcgis/rest/services/Definitive_Healthcare_USA_Hospital_Beds/FeatureServer/0/query"
    data = arcgis.get_data(url)

    # Create directory and initialize csv's if needed
    hospital_dir = pathlib.Path('hospital_data_time_series')
    if not hospital_dir.exists():
        init_folders(hospital_dir, data)

    # Get data for each feature
    for feature, config in features.items():
        desired_columns = join_keys + [feature]
        df = arcgis.json_to_df(data, desired_columns)

        groupby = config['groupby']
        states_df = groupby(df, ['STATE_NAME'])
        counties_df = groupby(df, ['COUNTY_NAME', 'STATE_NAME'])

        # Load current csvs with all old data
        csvf = config['csvfile']
        states_full_path = hospital_dir.joinpath('states').joinpath(csvf)
        counties_full_path = hospital_dir.joinpath('counties').joinpath(csvf)
        old_states_df = pd.read_csv(states_full_path, index_col=0)
        old_counties_df = pd.read_csv(counties_full_path, index_col=0)

        # Name new data column after today's date
        today = str(pd.to_datetime("today").date())
        states_df.rename(columns={feature: today}, inplace=True)
        counties_df.rename(columns={feature: today}, inplace=True)

        # Append todays data as a new column in old csv if it doesn't exist
        if today not in old_states_df:
            new_states_df = pd.merge(old_states_df, states_df, on=[
                'STATE_NAME'], how='outer')
            new_states_df.to_csv(states_full_path)
        if today not in old_counties_df:
            new_counties_df = pd.merge(old_counties_df, counties_df, on=[
                'STATE_NAME', 'COUNTY_NAME'], how='outer')
            new_counties_df.to_csv(counties_full_path)


# Initializes 'base_folder/counties/*.csv' and 'base_folder/states/*.csv'
def init_folders(base_folder, data):

    def init_csvs(folder, df):
        for feature_config in features.values():
            df.to_csv(folder.joinpath(feature_config['csvfile']))

    counties_folder = base_folder.joinpath('counties')
    states_folder = base_folder.joinpath('states')
    base_folder.mkdir()
    counties_folder.mkdir()
    states_folder.mkdir()

    states_cols = ['STATE_FIPS', 'STATE_NAME']
    counties_cols = ['CNTY_FIPS', 'STATE_FIPS', 'COUNTY_NAME', 'STATE_NAME']
    states_df = arcgis.json_to_df(data, states_cols)
    counties_df = arcgis.json_to_df(data, counties_cols)
    states_df.drop_duplicates(inplace=True)
    counties_df.drop_duplicates(inplace=True)

    init_csvs(states_folder, states_df)
    init_csvs(counties_folder, counties_df)


if __name__ == '__main__':
    main()
