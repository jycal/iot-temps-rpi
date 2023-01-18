import psutil, time, os, requests

updateInterval = 15  # update once every 15 seconds
writeAPIkey = "OY8DUS7XDPAU2KTT"  # write API key for the channel
channelID = "2003669"  # channel ID
# ThingSpeak url
URL = "https://api.thingspeak.com/update?api_key=OY8DUS7XDPAU2KTT"


def getData():
    """Function that returns the CPU temperature and percentage of CPU utilization"""
    cmd = 'cat /sys/class/thermal/thermal_zone0/temp'  # command to get the CPU temperature
    process = os.popen(cmd).readline().strip()
    cpuTemp = int(process.split('=')[0].split("'")[0]) / 1000 # get the CPU temperature
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
