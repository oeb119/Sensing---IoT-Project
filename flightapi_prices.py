# Set your API key before making the request
import pprint
import requests
import json
from datetime import datetime

def get_time():
    # Get the current date and time
    current_time = datetime.now()
    # Format the time into "day_hour_minute"
    formatted_time = current_time.strftime("%d_%H_%M")
    return formatted_time

#formatted_time = get_time()

def get_url(API_key, airport1, airport2, day):
    """Generate a url from a search term"""
    template = "https://api.flightapi.io/onewaytrip/{}/{}/{}/{}/1/0/0/Economy/USD"
    return template.format(API_key, airport1, airport2, day)

# API_key = "65675eef7c2715dd88f941a4"
# day = 21
# url = get_url(API_key, "LHR", "CDG", "2023-12-"+str(day))

def get_data(url):
    response = requests.get(url).json()
    # # Perform additional processing on the JSON response
    flights = json.dumps(response)
    # pprint.pprint(json.loads(flights), indent=2)
    return flights

# flights = get_data(url)

## Makes file name according to date
def get_file_name(day, formatted_time):
    file_name = "flightapi_dec_{}_2023_at_{}.csv".format(day, formatted_time)
    return file_name

# file_name = get_file_name(str(day), formatted_time)

## Saves flight info in json file
def save_file(file_name, flights):
    # Write the JSON data to the file
    with open(file_name, 'w') as file:
        file.write(json.dumps(json.loads(flights), indent=2))

# save_file(file_name, flights)


## GETTING THE MINIMUM FLIGHT INFO
def min_flight_price(file_name):
    with open(file_name, 'r') as file:
        data = json.loads(file.read())

    # Iterate through fares and find minimum trip id
    # Initialize variables to keep track of the minimum price and the associated trip ID
    min_price = float('inf')
    min_price_trip_id = None

    # Iterate through the fares
    for fare in data['fares']:
        total_amount_usd = fare['price']['totalAmountUsd']
        trip_id = fare['tripId']

        # Check if the current fare has a lower price
        if total_amount_usd < min_price:
            min_price = total_amount_usd
            min_price_trip_id = trip_id

    # Use the trip id to find the associated leg id
    leg_id = next((trip['legIds'][0] for trip in data['trips'] if min_price_trip_id in trip['id']), None)
    # Use the leg id to find the details of the trip
    leg = next((leg for leg in data['legs'] if leg_id in leg['id']), None)

    if leg:
        departure = leg['departureTime']
        duration = leg['duration']
        airline_code = leg['airlineCodes'][0]

    # Translate airline code to airline name
    airline = next((airline['name'] for airline in data['airlines'] if airline_code in airline['code']), None)
    return [min_price, departure, duration, airline]

# cheapest_flight = min_flight_price(file_name)
# print(cheapest_flight[0])