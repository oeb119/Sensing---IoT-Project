#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3

import requests
import edit_eurostar1_pi as eu
import flightapi_prices_pi as fl
import performance_time as pe
from datetime import datetime


### Starting timer ###

print('RUNNING AGGREGATE')
start_time = datetime.now()
print(start_time)


### FlightAPI Key graveyard... rip ###

API_key = "657774e157d0fa338ac2fb7f"
# OEB119 API 65675eef7c2715dd88f941a4 0 left
# ALEXI API 656dda2ab9700088b235a219 0 left
# ORIANE.BUI API 656f13b0c6eb315e7eecbc79 1 left
# OEB119@IC.AC.UK 65703d056c2bcd5e842ea53e 2 left
# MOLLY API 6570486c2b921b5e70890300 0 left
# CLEMENCE API 65704970dcc1295e71c872d0 2 left
# THARANY API 65704b262b921b5e70890301 2 left
# BAGGO API 65759c857c8bf3d205a36815 0 left
# GOOD API 65759d0132ec89d21b701280 0 left
# BLURB API 65759d957c8bf3d205a36816 0 left
# GOODTIMES API 65759dd328c0e6d20b72cc57 0 left
# ONEMORE API 65759e2e32ec89d21b701281 MAC
# CARPET API 657774f07ed3e7339996d80e RPI 0 left
# COUCH API 657774e157d0fa338ac2fb7f RPI
# TABLE API 6577747e30bad43384fc8f59 RPI
# CUPPA API 657774977ed3e7339996d80b RPI
# BOWL API 657774a157d0fa338ac2fb7e RPI
# BOOK API 657774aa7ed3e7339996d80c
# PHONE API 657774b52bb093339236b0c9
# PENCIL API 657774cc7ed3e7339996d80d
# CHAIR API 657774d530bad43384fc8f5b



### Function to get cheapest train ticket for given day ###

def cheapest_eurostar(day):
    formatted_time = eu.get_time()
    url = eu.get_url("7015400", "8727100", "2023-12-", str(day))
    driver = eu.create_driver()
    soup = eu.scrape_data(driver, url)
    trains = eu.trains_listings(soup)
    csv_name = eu.get_csv_name(day, formatted_time)
    print(csv_name)
    df = eu.dataframe(csv_name, trains)
    cheapest_train = eu.cheapest(df)
    eu.close_driver(driver)
    return cheapest_train


### Function to get cheapest plane ticket for given day ###

def cheapest_flight(API_key, day):
    formatted_time = fl.get_time()
    url = fl.get_url(API_key, "LTN", "CDG", "2023-12-"+str(day))
    flights = fl.get_data(url)
    file_name = fl.get_file_name(str(day), formatted_time)
    fl.save_file(file_name, flights)
    print(file_name)
    cheapest_flight = fl.min_flight_price(file_name)
    return cheapest_flight


### Functions defining how to write data to ThingSpeak API ###

eu_channel = ''
fl_channel = ''

def update_api(channel, field, update_value):
    requests.get(channel + str(field) + '=' + str(update_value))

def day_to_field(day):
    corresp = ['20', '21', '22', '23', '24', '25', '26', '27']
    field = corresp.index(str(day)) + 1
    return field


### Initializing empty lists into which price data for Dec 20 to 27th will go ###

list_trains = []
list_planes = []


### For loop to pull price data for every day, calling functions defined above and writing them to ThingSpeak API ###

for day in range(20,28):        
    print(day)
    cheapest_eurostar_result = cheapest_eurostar(day)
        
    print(cheapest_eurostar_result)

    counter = 0
    while not cheapest_eurostar_result:
        counter += 1
        if counter == 4:
            print("There are probably no trains on this day")
            cheapest_eurostar_result = []
            break
        print("Did not work so running agian")
        cheapest_eurostar_result = cheapest_eurostar(day)
        
    print("The cheapest Eurostar on " + str(day) + " is " + str(cheapest_eurostar_result))

    cheapest_flight_result = cheapest_flight(API_key, day)

    print("The cheapest flight on " + str(day) + " is " + str(cheapest_flight_result[4]))
    
    if day != 27:
        list_trains.append(cheapest_eurostar_result)
        list_planes.append(cheapest_flight_result)

    else:
        list_trains.append(cheapest_eurostar_result)
        list_planes.append(cheapest_flight_result)

        eu_channel = ''
        fl_channel = ''

        requests.get(eu_channel + '1=' + str(list_trains[0]) + "&field2=" + str(list_trains[1]) + "&field3=" + str(list_trains[2]) + "&field4=" + str(list_trains[3]) + "&field5=" + str(list_trains[4]) + "&field6=" + str(list_trains[5]) + "&field7=" + str(list_trains[6]) + "&field8=" + str(list_trains[7]))
        print(eu_channel + '1=' + str(list_trains[0]) + "&field2=" + str(list_trains[1]) + "&field3=" + str(list_trains[2]) + "&field4=" + str(list_trains[3]) + "&field5=" + str(list_trains[4]) + "&field6=" + str(list_trains[5]) + "&field7=" + str(list_trains[6]) + "&field8=" + str(list_trains[7]))
        requests.get(fl_channel + '1=' + str(list_planes[0][4]) + "&field2=" + str(list_planes[1][4]) + "&field3=" + str(list_planes[2][4]) + "&field4=" + str(list_planes[3][4]) + "&field5=" + str(list_planes[4][4]) + "&field6=" + str(list_planes[5][4]) + "&field7=" + str(list_planes[6][4]) + "&field8=" + str(list_planes[7][4]))
        print(fl_channel + '1=' + str(list_planes[0][4]) + "&field2=" + str(list_planes[1][4]) + "&field3=" + str(list_planes[2][4]) + "&field4=" + str(list_planes[3][4]) + "&field5=" + str(list_planes[4][4]) + "&field6=" + str(list_planes[5][4]) + "&field7=" + str(list_planes[6][4]) + "&field8=" + str(list_planes[7][4]))
        
        # update_api(eu_channel, day_to_field(day), cheapest_eurostar_result)
        # print(eu_channel + str(day_to_field(day)) + '=' + str(cheapest_eurostar_result))
        # update_api(fl_channel, day_to_field(day), cheapest_flight_result[0])
        # print(fl_channel + str(day_to_field(day)) + '=' + str(cheapest_flight_result[0]))


### Ending timer, calculating time difference and writing it to ThingSpeak API ###
end_time = datetime.now()
time = end_time - start_time
time_seconds = time.total_seconds()
print(time_seconds)
pe.add_to_csv(start_time, end_time, time)
requests.get(''+ str(time_seconds))