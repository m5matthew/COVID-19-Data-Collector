import requests
import pandas as pd


# Convert ArcGIS json output to a dataframe
def json_to_df(json_data, desired_columns):
    data = [x['attributes'] for x in json_data['features']]
    df = pd.DataFrame(data)
    df = df[desired_columns]
    return df


# Rename dataframe to default alias names provided by ArcGIS
def rename_to_default_alias(df, json_data):
    headers = {}
    for x in json_data['fields']:
        headers[x['name']] = x['alias']
    df.rename(columns=headers, inplace=True)
    return df


# Get data from ArcGIS API
# # Offical Documentation: https://developers.arcgis.com/rest/services-reference/query-feature-service-layer-.htm
def get_data(url):
    query = {
        'f': 'json',
        'outFields': '*',
        'returnGeometry': 'false',
        'where': '1=1'
    }
    data = requests.post(url, data=query)
    return data.json()
