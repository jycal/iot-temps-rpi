import time
import os
import requests
from sense_hat import SenseHat

updateInterval = 15  # update once every 15 seconds
writeAPIkey = "OY8DUS7XDPAU2KTT"  # write API key for the channel
channelID = "2003669"  # channel ID
# ThingSpeak url
URL = "https://api.thingspeak.com/update?api_key=OY8DUS7XDPAU2KTT"


def getData():
    """Function that returns the temperature and humidity"""
    sense = SenseHat()
    sense.clear()

    humid_temp = sense.get_temperature_from_humidity()
    press_temp = sense.get_temperature_from_pressure()
    cmd = 'cat /sys/class/thermal/thermal_zone0/temp'  # command to get the CPU temperature
    process = os.popen(cmd).readline().strip()
    cpu_temp = int(process.split('=')[0].split("'")[0]) / 1000 # get the CPU temperature
    mid_temp = (humid_temp + press_temp) / 2  # avg temp from different sensors
    temp = mid_temp - ((cpu_temp - mid_temp) / 1.5)

    return round(temp)


def postData():
    temp = getData()

    response = requests.post(URL + '&field1=' + str(temp))
    if response:
        print('Succes!')
    else:
        print('Error occurred!')


if __name__ == '__main__':
    while True:
        time.sleep(updateInterval)
        postData()
