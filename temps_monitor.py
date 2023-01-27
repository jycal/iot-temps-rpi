import time
import os
import requests
from sense_hat import SenseHat

updateInterval = 300  # update once every 5 minutes
writeAPIkey = 'OY8DUS7XDPAU2KTT'  # write API key for the channel
readAPIkey = 'TXI2BWJFGPTIVELP'  # read API key for the channel
channelID = '2003669'  # channel ID


def sensorData():
    """Function that returns the temperature and humidity"""
    sense = SenseHat()
    sense.clear()

    sense_temp = sense.temp
    # command to get the CPU temperature
    cmd = 'cat /sys/class/thermal/thermal_zone0/temp'
    process = os.popen(cmd).readline().strip()
    cpu_temp = int(process.split('=')[0].split(
        "'")[0]) / 1000  # get the CPU temperature
    temp = sense_temp - (cpu_temp - sense_temp)

    return temp


def getData():
    """Function that returns the data from the ThingSpeak channel"""
    URL = "https://api.thingspeak.com/channels/" + channelID + "/feeds.json?api_key=" + readAPIkey + "&results=8000"
    response = requests.get(URL)
    if response:
        print('GET Succes!')
    else:
        print('Error occurred!')

    data = response.json()

    return data


def postData():
    """Function that posts the data to the ThingSpeak channel"""
    temp = sensorData()
    feeds = getData()['feeds']
    temps = []
    first = True

    for feed in feeds:
        if feed['field1'] != 'None':  # check if the field is empty
            first = False
            temps.append(float(feed['field1']))

    if not first:
        avgTemp = sum(temps) / len(temps)  # calculate the average temperature
        minTemp = min(temps)  # calculate the minimum temperature
        maxTemp = max(temps)  # calculate the maximum temperature

    if first:
        fields = '&field1=' + str(temp)
    else:
        stats = '&field2=' + str(avgTemp) + '&field3=' + str(minTemp) + '&field4=' + str(maxTemp)
        fields = '&field1=' + str(temp) + stats

    response = requests.post('https://api.thingspeak.com/update?api_key=' + writeAPIkey + fields)
    if response:
        print('POST Succes!')
    else:
        print('Error occurred!')


if __name__ == '__main__':
    while True:
        time.sleep(updateInterval)
        postData()
