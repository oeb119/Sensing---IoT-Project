import csv
import requests
from datetime import datetime

def add_to_csv(start, end, time):
    try:
        print(str(time))
        time_seconds = time.total_seconds()
        data = [start, end, time_seconds]

        with open('Performance_time.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    except Exception as e:
        print(f"An error occurred: {e}")

# start_time = datetime.now()
# end_time = datetime.now()
# time = end_time - start_time
# add_to_csv(start_time, end_time, time)

# requests.get('https://api.thingspeak.com/update?api_key=2YUCM035QX3XXF0J&field1='+ str(time))