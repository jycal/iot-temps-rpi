## Introduction

This is a Rasberry Pi project for my Data Science for IoT class. It uses a Sense HAT to send data to ThingSpeak. I've used a Raspberry Pi 4 Model B and a Snse HAT for this project. The Python version is 3.9.2.

## The Idea

During these times the gas prices have risen up so I thought that a **Sense HAT** could be implemented in some way to be useful. My sleeping room is on the third floor while the thermostat is in the living room. My room is pretty cold so if I place my Raspberry Pi there, I can adjust the thermostat and rest before I go to my room. I can keep track of how warm my room by looking through my ThingSpeak channel view on my phone because the readings are uploaded to ThingSpeak.

![animated_sense_hat](https://user-images.githubusercontent.com/98151689/214977208-5eb85727-5235-4802-861c-6f976d1720a1.gif)

*"Sense HAT" - gif source: raspberrypi.org*

## Tutorial

Things you need:
- A Raspberry Pi that is compatible with Sense HAT (...and the power supply that you get when buying a Raspberry Pi but that's a given.)

   *(All Raspberry Pi's with 40 pin (2x20) connectors, including the Raspberry Pi 4, Pi 33, Raspberry Pi 2, Model B+, and Model A+, but NOT the earlier 26-pin models of Raspberry Pi 1 Model B & A's.)*  

- A Sense HAT
- A [ThingSpeak](https://thingspeak.com/) account

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
Download [temps_monitor.py](https://github.com/jycal/iot-temps-rpi/blob/main/temps_monitor.py).
Insert your own write API key, read API key and channel ID. 

![image](https://user-images.githubusercontent.com/98151689/214980503-eb591f69-6db0-40a8-896e-80cb98641be4.png)

The information is found in the API Keys tab.

![api](https://user-images.githubusercontent.com/98151689/214980922-7390fada-304c-4d89-894a-434a2c9c3374.png)

You should see something like this after you let the file run for a while:

![image](https://user-images.githubusercontent.com/98151689/214982768-0d7e6bc0-c652-4a47-8c77-3a3e2ed3e061.png)
