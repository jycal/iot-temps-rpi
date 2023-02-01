## Introduction

This is a Rasberry Pi project for my Data Science for IoT class. It uses a Sense HAT to send data to ThingSpeak. I've used a Raspberry Pi 4 Model B and a Snse HAT for this project. The Python version is 3.9.2.

## The Idea

During these times the gas prices have risen up so I thought that a Sense HAT could be implemented in some way to be useful. I knew about the Sense HAT because I have worked with it before but I've only tested a few functions. 

Ok, so the thing is that my sleeping room is on the third floor while the thermostat is in the living room. My room gets pretty cold because the temperature is adjusted to only warm the living room because nobody is upstairs. So if I place my Raspberry Pi in my sleeping room, I can adjust the thermostat and rest in the living room before I go to my room. I can keep track of how warm my room by looking through my ThingSpeak channel view on my phone because the readings are uploaded to ThingSpeak.

## The Climb

I made a test file in the beginning to see how you POST to ThingSpeak. I found out that you can send to mutiple field by just concatenating *'&field1='* and *'&field1='*.
```python
import psutil
import time
import os
import requests

updateInterval = 15  # update once every 15 seconds
writeAPIkey = "OY8DUS7XDPAU2KTT"  # write API key for the channel
channelID = "2003669"  # channel ID
# ThingSpeak url
URL = "https://api.thingspeak.com/update?api_key=OY8DUS7XDPAU2KTT"


def getData():
    """Function that returns the CPU temperature and percentage of CPU utilization"""
    cmd = 'cat /sys/class/thermal/thermal_zone0/temp'  # command to get the CPU temperature
    process = os.popen(cmd).readline().strip()
    cpuTemp = int(process.split('=')[0].split("'")[0]) / 1000  # get the CPU temperature
    cpuUsage = psutil.cpu_percent(interval=2)  # get the CPU usage

    return cpuTemp, cpuUsage


def postData():
    temp, usage = getData()

    response = requests.post(URL + '&field1=' + str(temp) + '&field2=' + str(usage))
    if response:
        print('Succes!')
    else:
        print('Error occurred!')


if __name__ == '__main__':
    while True:
        time.sleep(updateInterval)
        postData()
```
Then I started to make the function that has the temperature sensor of the Sense HAT be used.
I found out that the temperature sensor wasn't accurate due the fact that it's above the CPU.
I tried to get the temperatures from the humidity sensor, pressure sensor and cpu to see if they had an impact on the the temperature reading. I got the divide by 1.5 from an obscure forum post where people discussed the same problem they had with the temperature sensor:
```python
sense = SenseHat()
sense.clear()

humid_temp = sense.get_temperature_from_humidity()
press_temp = sense.get_temperature_from_pressure()
cmd = 'cat /sys/class/thermal/thermal_zone0/temp'  # command to get the CPU temperature
process = os.popen(cmd).readline().strip()
cpu_temp = int(process.split('=')[0].split("'")[0]) / 1000  # get the CPU temperature
mid_temp = (humid_temp + press_temp) / 2  # avg temp from different sensors
temp = mid_temp - ((cpu_temp - mid_temp) / 1.5)
```
That didn't help at all so in the end I found out that I could just subtract temperature from the Sense HAT from the CPU temperature and then subract that result from the temperature from the Sense HAT to get a better reading.
```python
sense = SenseHat()
sense.clear()

sense_temp = sense.temp
# command to get the CPU temperature
cmd = 'cat /sys/class/thermal/thermal_zone0/temp'
process = os.popen(cmd).readline().strip()
cpu_temp = int(process.split('=')[0].split(
    "'")[0]) / 1000  # get the CPU temperature
temp = sense_temp - (cpu_temp - sense_temp)
```
After being done with that I wanted to be able to see average, minimum and maximum temperature. I wasn't able to retrieve more than one JSON after sending a GET request but I found out that all I needed to do was change results from 1 to 8000.
```python
URL = "https://api.thingspeak.com/channels/" + channelID + "/feeds.json?api_key=" + readAPIkey + "&results=8000"
```
Updating my GitHub repository was something I did once I was done or satisfied with certain things. I made a To-Do list for things I have to add to the README to keep me on track.

My ThingSpeak channel: https://thingspeak.com/channels/2003669

## Conclusion

Using the Sense HAT was quite an adventure due to the fact it has inaccurate readings when not calibrating the readings. I learned a lot about the Sense HAT and how to work with ThingSpeak to send data and retrieve data. I think I could've improved the readings by modifying the Sense HAT postion to be elevated enought to not be afflicted by the CPU temperature could help in theory, but I'm pleased enough to have made a somewhat accurate Data Science IoT device because it retrieves temperature from a sensor, it processes the data and sends it to an API to be visualized so that you can judge whether or not adjust room temperature. 

## Video Demo

https://user-images.githubusercontent.com/98151689/215357620-1f8b1f82-5697-4525-bf4e-43667307dfb5.mp4

*Music: Untitled by Horse Lords - From the Free Music Archive, CC BY-NC-ND 4.0*

## Tutorial

Things you need:
- A Raspberry Pi that is compatible with Sense HAT (...and the power supply that you get when buying a Raspberry Pi but that's a given.)

   *(All Raspberry Pi's with 40 pin (2x20) connectors, including the Raspberry Pi 4, Pi 33, Raspberry Pi 2, Model B+, and Model A+, but NOT the earlier 26-pin models of Raspberry Pi 1 Model B & A's.)*  

- A Sense HAT
- A [ThingSpeak](https://thingspeak.com/) account

![animated_sense_hat](https://user-images.githubusercontent.com/98151689/214977208-5eb85727-5235-4802-861c-6f976d1720a1.gif)

*"Sense HAT" - gif source: raspberrypi.org*

### ThingSpeak

Create a channel on [ThingSpeak](https://thingspeak.com/).

![image](https://user-images.githubusercontent.com/98151689/214981519-557914fe-257a-4add-bfa6-2c5b661b0b96.png)

The next step is to make four fields.

![image](https://user-images.githubusercontent.com/98151689/214981701-95b221ce-4af0-4538-bc5b-07f01f3581f9.png)

Don't forget to save the channel.

![image](https://user-images.githubusercontent.com/98151689/214981938-6e5b0b2c-a79c-432d-853c-5e13dda55d42.png)

Now create a Numeric Display widgets for each field for easier reading.

![image](https://user-images.githubusercontent.com/98151689/214987254-8807afd1-c4b0-4281-9e36-d70af3c310ea.png)

![image](https://user-images.githubusercontent.com/98151689/214987262-4d11876e-5eab-4a21-8b6e-30100535b554.png)

Choose the field and put Celcius as the unit. Don't forget to put the data type as decimals.

![image](https://user-images.githubusercontent.com/98151689/214987615-85f161f7-be27-429c-950d-b12241985619.png)

### Code
Download [temps_monitor.py](https://github.com/jycal/iot-temps-rpi/blob/main/temps_monitor.py) on your Raspberry Pi by using the browser.
Insert your own write API key, read API key and channel ID. 

![image](https://user-images.githubusercontent.com/98151689/214980503-eb591f69-6db0-40a8-896e-80cb98641be4.png)

The information is found in the API Keys tab.

![api](https://user-images.githubusercontent.com/98151689/214980922-7390fada-304c-4d89-894a-434a2c9c3374.png)

You should see something like this after you let the file run for a while:

![image](https://user-images.githubusercontent.com/98151689/214982768-0d7e6bc0-c652-4a47-8c77-3a3e2ed3e061.png)
