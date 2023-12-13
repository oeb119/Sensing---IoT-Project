import psutil
import matplotlib.pyplot as plt
import datetime
import time
import requests

# Initialize empty lists for time and CPU usage
timestamps = []
cpu_usage = []

# Function to collect and log data
def collect_data():
    timestamps.append(datetime.datetime.now())
    cpu_usage.append(psutil.cpu_percent(interval=1))
    requests.get('https://api.thingspeak.com/update?api_key=2YUCM035QX3XXF0J&field2='+ str(psutil.cpu_percent(interval=1)))

# Run data collection for a specified duration
duration_minutes = 30
end_time = time.time() + 60 * duration_minutes

while time.time() < end_time:
    collect_data()

# Plot the collected data
plt.plot(timestamps, cpu_usage, marker='o')
plt.title('CPU Usage Over Time')
plt.xlabel('Time')
plt.ylabel('CPU Usage (%)')
plt.show()
