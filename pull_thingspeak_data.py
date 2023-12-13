import requests
import pandas as pd
import matplotlib.pyplot as plt

### Initializing credentials ###

eu_channel = '2363580'
fl_channel = '2367228'
eu_api_read = 'I0TX348P2XLD2V55'
fl_api_read = '5DMSQSY2KYNGH5ZD'


### Function to grab most recent price from ThingSpeak API ###

def get_latest_price(channel, field, api):

    def get_url(channel, field, api):
        """Generate a url from a search term"""
        template = 'https://api.thingspeak.com/channels/{}/fields/{}?api_key={}'
        return template.format(channel, field, api)

    url = get_url(channel, field, api)
    # Make an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data from the response
        json_data = response.json()
        print(json_data)
        field_name = "field{}".format(field)

        # Filter out entries where field1 is null
        filtered_data = [entry for entry in json_data["feeds"] if entry.get(field_name) is not None and entry[field_name] != '[]']
        
        print(filtered_data)
        # # Print the filtered data
        # for entry in filtered_data:
        #     print(entry)

        if filtered_data != []:
            # Print the last entry data
            print(filtered_data[len(filtered_data)-1][field_name])
            return filtered_data[len(filtered_data)-1][field_name]
        else:
            return False

    else:
        print(f'Error: {response.status_code}')

# print(get_latest_price(eu_channel, 1, eu_api_read))
# print(get_latest_price(fl_channel, 2, fl_api_read))


### Function to get dataframe of ticket prices and times found for requested day ###
### This will be used to make graphs of the data ###

def get_prices(channel, field, api):

    def get_url(channel, field, api):
        """Generate a url from a search term"""
        template = 'https://api.thingspeak.com/channels/{}/fields/{}?api_key={}'
        return template.format(channel, field, api)

    url = get_url(channel, field, api)
    # Make an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data from the response
        df = response.json()

        field_name = "field{}".format(field)

        # Filter out entries where field1 is null
        df = [entry for entry in df["feeds"] if entry.get(field_name) is not None and entry[field_name] != '[]']

        # Remove null values
        # df = df.dropna(subset=['field3'])

        # Convert 'created_at' to datetime format
        for entry in df:
            entry['created_at'] = pd.to_datetime(entry['created_at'])
            entry[field_name] = pd.to_numeric(entry[field_name], errors='coerce')

        return df

    else:
        print(f'Error: {response.status_code}')