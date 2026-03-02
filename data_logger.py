#!/home/don/python/bin/python3
# by Don Bales
# on 2025-12-22

from datetime import datetime
from email.message import EmailMessage
import os
from pathlib import Path
import RPi.GPIO as GPIO
import subprocess
import smtplib
import sys
import time

sys.stdout = open('/home/don/garden/data_logger.log', 'at')
sys.stderr = open('/home/don/garden/data_logger.err', 'at')

omask = os.umask(0o000)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

channel_list = [20,21]
GPIO.setup(channel_list, GPIO.OUT)

ACTUATOR_EAST = 21
ACTUATOR_WEST = 20

class Data:
    def __init__(self, dt):
        self.sample_date = (str(dt.year) + '-' + \
                            str(dt.month).rjust(2, '0') + '-' + \
                            str(dt.day).rjust(2, '0') + ' ' + \
                            str(dt.hour).rjust(2, '0') + ':' + \
                            str(dt.minute).rjust(2, '0') + ':' + \
                            str(dt.second).rjust(2, '0'))
    def __str__(self):
        return ('Data(actuator_east:  ' + str(self.actuator_east)  + "\n" + \
                '     actuator_west:  ' + str(self.actuator_west)  + "\n" + \
                '     moisture:       ' + str(self.moisture)       + "\n" + \
                '     sample_date:    ' + str(self.sample_date)    + "\n" + \
                '     temp_air_east:  ' + str(self.temp_air_east)  + "\n" + \
                '     temp_soil_east: ' + str(self.temp_soil_east) + "\n" + \
                '     temp_air_west:  ' + str(self.temp_air_west)  + "\n" + \
                '     temp_soil_west: ' + str(self.temp_soil_west) + "\n" + \
                '     temp_outside:   ' + str(self.temp_outside)   + "\n" + \
                '     temp_rpi:       ' + str(self.temp_rpi)       + ")\n")
    def to_json(self):
        return ('{"sample_date": "'    + str(self.sample_date)    + '",' + \
                ' "actuator_east": "'  + str(self.actuator_east)  + '",' + \
                ' "actuator_west": "'  + str(self.actuator_west)  + '",' + \
                ' "moisture": "'       + str(self.moisture)       + '",' + \
                ' "temp_air_east": "'  + str(self.temp_air_east)  + '",' + \
                ' "temp_soil_east": "' + str(self.temp_soil_east) + '",' + \
                ' "temp_air_west": "'  + str(self.temp_air_west)  + '",' + \
                ' "temp_soil_west": "' + str(self.temp_soil_west) + '",' + \
                ' "temp_outside": "'   + str(self.temp_outside)   + '",' + \
                ' "temp_rpi": "'       + str(self.temp_rpi)       + '"}\n')
    def to_tsv(self):
        return (str(self.sample_date)    + "\t" + \
                str(self.actuator_east)  + "\t" + \
                str(self.actuator_west)  + "\t" + \
                str(self.moisture)       + "\t" + \
                str(self.temp_air_east)  + "\t" + \
                str(self.temp_soil_east) + "\t" + \
                str(self.temp_air_west)  + "\t" + \
                str(self.temp_soil_west) + "\t" + \
                str(self.temp_outside)   + "\t" + \
                str(self.temp_rpi)       + "\n")
    actuator_east = 'Closed'
    actuator_west = 'Closed'
    moisture = 0
    sample_date = None
    temp_air_east = None
    temp_air_west = None
    temp_moisture = None
    temp_outside = None
    temp_rpi = None
    temp_soil_east = None
    temp_soil_west = None

difference = 1.5
germ_yyyy_mm_dd = '2025-12-22'
grow_yyyy_mm_dd = '2026-01-02'
on_five_minutes = (0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55)
one_minute_before = (4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59)
temp_max_germ = 85
temp_max_grow = 75
thermometer_dir = '/sys/bus/w1/devices/'
thermometers = ('28-02c3d4460f6d','28-1b16d446ac0a','28-395dd4461902','28-427ed446d918','28-67cad44668c1')

def rpi_temp():
    completed_process = subprocess.run(['/usr/bin/vcgencmd', ' measure_temp'], capture_output=True)
    #print(completed_process, flush=True);
    output = str(completed_process.stdout)
    #print(output, flush=True)
    equals_pos = output.find('=')
    #print(equals_pos, flush=True)
    tic_pos = output.find("'")
    #print(tic_pos, flush=True)
    c = float(output[equals_pos + 1:tic_pos])
    f = round((c * 9.0 / 5.0) + 32.0, 2)
    #print("RPi Temp: ", c, f, flush=True)
    return f

def send_notification(body):
    message = EmailMessage()
    message.set_content(body)
    message['Subject'] = "raspberrypi-3-garden Alert"
    message['From'] = 'don@donaldbales.com'
    message['To'] = 'donaldbales@mac.com'
    # creates SMTP session
    connection = smtplib.SMTP('netsol-smtp-oxcs.hostingplatform.com', 587)
    # start TLS for security
    connection.starttls()
    # Authentication
    connection.login("don@donaldbales.com", os.getenv('EMAIL_PASSWORD', ''))
    # sending the mail
    connection.sendmail("don@donaldbales.com", "donaldbales@mac.com", message.as_string())
    # terminating the session
    connection.quit()
    return True

def ymd_path(dt):
    return '/home/don/data/' + str(dt.year) + '/' + str(dt.month).rjust(2, '0') + '/' + str(dt.day).rjust(2, '0')

def ymdh_filename(dt):
    return str(dt.year) + str(dt.month).rjust(2, '0') + str(dt.day).rjust(2, '0') + str(dt.hour).rjust(2, '0') + '.tsv'

def read_temp_raw(thermometer):
    device_file = thermometer_dir + thermometer + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp(thermometer):
    lines = read_temp_raw(thermometer)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = round(float(temp_string) / 1000.0, 2)
        temp_f = round((temp_c * 9.0 / 5.0) + 32.0, 2)
        return temp_c, temp_f

def write_data(dt, data):
    data_path = Path(ymd_path(dt))
    if (not data_path.exists()):
        result = data_path.mkdir(mode=0o777, parents=True)
        #print(result, flush=True)
    data_file = ymd_path(dt) + '/' + ymdh_filename(dt)
    file_object = open(data_file, 'a')
    file_object.write(data.to_tsv())
    file_object.close()

try:
    while True:
        dt = datetime.now()
        d_yyyy_mm_dd = dt.isoformat()[:10]

        # Try to align to five minute, zero seconds
        while (dt.minute in one_minute_before and \
               dt.second >= 29):
            #print(str(dt.second), flush=True)
            time.sleep(1)
            dt = datetime.now()
            d_yyyy_mm_dd = dt.isoformat()[:10]
            #print(dt, flush=True)
            #print(d_yyyy_mm_dd, flush=True)
        data = Data(dt)
        #print(str(data.sample_date), flush=True)
        data.temp_rpi = rpi_temp()
        for i in range(5):
            thermometer = thermometers[i]
            try:
                c, f = read_temp(thermometer)
            except Exception as error:
                c = None
                f = None
                print('Error reading thermometer ' + str(i) + ' ' + thermometer + ': ' + str(error), flush=True)
                print('Error reading thermometer ' + str(i) + ' ' + thermometer + ': ' + str(error), file=sys.stderr, flush=True)
            #print(thermometer, c, f, flush=True)
            if   (thermometer == thermometers[0]):
                data.temp_air_east = f
            elif (thermometer == thermometers[1]):
                data.temp_soil_east = f
            elif (thermometer == thermometers[2]):
                data.temp_air_west = f
            elif (thermometer == thermometers[3]):
                data.temp_soil_west = f
            elif (thermometer == thermometers[4]):
                data.temp_outside = f

        if (data.temp_air_east  is None or \
            data.temp_soil_east is None or \
            data.temp_air_west  is None or \
            data.temp_soil_west is None or \
            data.temp_outside   is None):
            send_notification("RPi has lost communication with a sensor.")

        #if (data.temp_air_east is not None and \
        #    data.temp_air_east > 95.0):
        #    send_notification("The east air temperature is over 95 degrees.")
        #    
        #if (data.temp_air_west is not None and \
        #    data.temp_air_west > 95.0):
        #    send_notification("The west air temperature is over 95 degrees.")
            
        if (d_yyyy_mm_dd < germ_yyyy_mm_dd):
            print("Before germination. Closing both lids..", flush=True)
            # if it is before the germination start date
            # close the lids to warm up the soil
            GPIO.output(ACTUATOR_EAST, GPIO.LOW)
            time.sleep(1)
            GPIO.output(ACTUATOR_WEST, GPIO.LOW)

        elif (d_yyyy_mm_dd < grow_yyyy_mm_dd):
            print("Germinating...", flush=True)
            # if it is after the germination start date
            # and before the growth start date
            # regulate to temperature to maximize germination
            if (data.temp_air_east is not None and \
                data.temp_air_east > temp_max_germ):
                print("Opening east lid.", flush=True)
                data.actuator_east = 'Open'
                GPIO.output(ACTUATOR_EAST, GPIO.HIGH)
            elif (data.temp_air_east is not None and \
                  data.temp_air_east <= temp_max_germ - difference):
                print("Closing east lid.", flush=True)
                data.actuator_east = 'Closed'
                GPIO.output(ACTUATOR_EAST, GPIO.LOW)
            else:
                print("Cooling, east lid open.", flush=True)
                data.actuator_east = 'Open'
                GPIO.output(ACTUATOR_EAST, GPIO.HIGH)
            time.sleep(1)
            if (data.temp_air_west is not None and \
                data.temp_air_west > temp_max_germ):
                print("Opening west lid.", flush=True)
                data.actuator_west = 'Open'
                GPIO.output(ACTUATOR_WEST, GPIO.HIGH)
            elif (data.temp_air_west is not None and \
                  data.temp_air_west <= temp_max_germ - difference):
                print("Closing west lid.", flush=True)
                data.actuator_west = 'Closed'
                GPIO.output(ACTUATOR_WEST, GPIO.LOW)
            else:
                print("Cooling, west lid open.", flush=True)
                data.actuator_west = 'Open'
                GPIO.output(ACTUATOR_WEST, GPIO.HIGH)
        else:
            print("Growing...", flush=True)
            # if it is after the germination start date
            # and after the growth start date
            # regulate to temperature to maximize growth
            if (data.temp_air_east is not None and \
                data.temp_air_east > temp_max_grow):
                print("Opening east lid.", flush=True)
                data.actuator_east = 'Open'
                GPIO.output(ACTUATOR_EAST, GPIO.HIGH)
            elif (data.temp_air_east is not None and \
                  data.temp_air_east <= temp_max_grow - difference):
                print("Closing east lid.", flush=True)
                data.actuator_east = 'Closed'
                GPIO.output(ACTUATOR_EAST, GPIO.LOW)
            else:
                print("Cooling, east lid open.", flush=True)
                data.actuator_east = 'Open'
                GPIO.output(ACTUATOR_EAST, GPIO.HIGH)
            time.sleep(1)
            if (data.temp_air_west is not None and \
                data.temp_air_west > temp_max_grow):
                print("Opening west lid.", flush=True)
                data.actuator_west = 'Open'
                GPIO.output(ACTUATOR_WEST, GPIO.HIGH)
            elif (data.temp_air_west is not None and \
                  data.temp_air_west <= temp_max_grow - difference):
                print("Closing west lid.", flush=True)
                data.actuator_west = 'Closed'
                GPIO.output(ACTUATOR_WEST, GPIO.LOW)
            else:
                print("Cooling, west lid open.", flush=True)
                data.actuator_west = 'Open'
                GPIO.output(ACTUATOR_WEST, GPIO.HIGH)

        print(data.to_json(), flush=True)

        if (dt.minute in on_five_minutes and \
            dt.second <= 29) or \
            data.actuator_east == 'Open' or \
            data.actuator_west == 'Open':
            print('Writing data for ' + data.sample_date, flush=True)
            try: 
                write_data(dt, data)
            except Exception as error:
                print('Error writing data ' + data.to_json() + ': ' + str(error), flush=True)
                print('Error writing data ' + data.to_json() + ': ' + str(error), file=sys.stderr, flush=True)

        # Wait for 29 seconds
        time.sleep(29);

except KeyboardInterrupt:
    os.umask(omask)
    # Clean up the GPIO pins on exit
    GPIO.cleanup()
    #print("Program exited cleanly", flush=True)
