import math
import speedtest
import requests

#pip3 install speedtest-cli

def bytes_to_mb(size_bytes):
    i = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, i)
    size = round(size_bytes / power, 2)
    return f"{size} Mbps"

def get_internet_speed():
    wifi = speedtest.Speedtest()

    print("download speed...")
    download_speed = bytes_to_mb(wifi.download())

    print("upload speed...")
    upload_speed = bytes_to_mb(wifi.upload())

    requests.get('https://api.thingspeak.com/update?api_key=2YUCM035QX3XXF0J&field3='+ str(download_speed) + '&field4='+ str(upload_speed))
    print("download:", download_speed)
    print("upload:", upload_speed)

get_internet_speed()