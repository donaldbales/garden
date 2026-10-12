# Raspberry Pi In The Garden


## Links

Raspberry Pi

https://www.raspberrypi.com/

Raspberry Pi GPIO

https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio

https://pinout.xyz/pinout/gpio

Adafruit Sensors

https://www.adafruit.com/


## Steps

1. Acquire Parts
2. Install the Raspberry Pi Imager on your computer
3. Run the Raspberry Pi Imager
4. Find the RPi on the network
5. Enable Admin Password
6. Enable VNC
7. Enable SPI (if needed)
8. Enable I2C (if needed)
9. Enable 1-Wire (if needed)
10. Verify the configuration
11. Verify the hardware
12. Install Python
13. Install pip
14. Use Pip to install sensor drivers
15. Install an I2C hardware clock
16. Install an I2C soil sensor
17. Install a 1-Wire thermometer
18. Install a relay hat
19. Python Resources
20. Git
21. Create a program to read the soil sensor
22. Create a program to read the 1-Wire thermometer
23. Create a program to turn relays on and off
24. Create a data collection program
25. Create a data transmission program
26. Set email password in root environment
27. Create a daemon configuration file
28. Start the daemon
29. Restart the daemon
30. Set the daemon to autostart on boot
31. Stop the daemon
32. Backup
33. Data Receiver


### Acquire Parts

Acquire a Raspberry Pi Model 3+ (RPi)

https://www.adafruit.com/product/3775

Acquire a set of heat sinks for the RPi

https://www.adafruit.com/product/3082

Acquire a 2.5A micro USB power supply for the RPi

https://www.adafruit.com/product/1995

Acquire a HMDI video cable

https://www.amazon.com/dp/B016CIYOAA

Acquire a fast (Read 180mb/s, Write 130MB/s) micro SD card (I like Samsung PRO-Plus 128GB)

https://www.amazon.com/Samsung-microSDXC-Nintendo-Switch-MB-MD1T0SA-LC1/dp/B0DQX3136M

You' also need a USB keyboard, mouse, and HDMI display

https://www.amazon.com/dp/B017M4J1BU

Use your TV for a display

-OR-

https://www.amazon.com/Eyoyo-Monitor-1024x768-Resolution-Portable/dp/B01FHDL1DE


### Install the Raspberry Pi Imager on your computer

https://www.raspberrypi.com/software/


### Run the Raspberry Pi Imager

To create a 64bit operating system image on the micro SD card:

1. Plug the microSD card into your computer
2. Choose Device: Raspberry Pi 3, then Next
3. Choose Raspberry Pi OS (64-bit), then Next
4. Choose the SD card you plugged into your computer, then Next
5. Specify a host name, for example: raspberrypi-3-202610011, then Next
6. Specify the time zone, for example: America/Phoenix
7. Specify the keyboard layout, for example: us, then Next
8. Specify a username, for example: rpi
9. Specify a password, for example: teekieThe3to (this was generated raandomly using: pwgen 12 1)
10. Confirm the password, then Next
11. Specify an SSID (wifi network name)
12. Specify the password (wifi network password), then Next
13. Enable SSH
14. Use password authentication, then Next
15. Leave Raspberry Pi Connect off, then Next
16. Verify your settings, then Write
17. Then Finish
18. Remove the microSD card from your computer
19. Install the microSD card in the RPi
20. Plug the RPi in to boot


### Find the RPi on the network

```
sudo nmap -A -p22 -sS 192.168.0.0/24 2>/dev/null | grep "scan"
```

Make a note of it.


### Enable Admin Password

1. Log into the RPi using ssh rpi@\<ip address>
2. Run sudo ``` raspi-config ```
3. Choose: 1 System Options
4. Choose: S10 Admin Password
5. Choose: Yes
6. Choose: OK
7. Choose: Finish


### Enable VNC

1. Log into the RPi using ssh rpi@\<ip address>
2. Run sudo ``` raspi-config ```
3. Choose: 3 Interface Options
4. Choose: I3 VNC
5. Choose: Yes
6. Choose: OK
7. Choose: Finish


### Enable SPI

1. Log into the RPi using ssh rpi@\<ip address>
2. Run sudo ``` raspi-config ```
3. Choose: 3 Interface Options
4. Choose: I4 SPI
5. Choose: Yes
6. Choose: OK
7. Choose: Finish


### Enable I2C

1. Log into the RPi using ssh rpi@\<ip address>
2. Run sudo ``` raspi-config ```
3. Choose: 3 Interface Options
4. Choose: I5 I2C
5. Choose: Yes
6. Choose: OK
7. Choose: Finish


### Enable 1-Wire

1. Log into the RPi using ssh rpi@\<ip address>
2. Run: sudo ``` raspi-config ```
3. Choose: 3 Interface Options
4. Choose: I7 1-Wire
5. Choose: Yes
6. Choose: OK
7. Choose: Finish


### Verify Configuration

1. Log into the RPi using ssh rpi@<ip address>
2. Run: ``` cat /boot/firmware/config.txt ```
3. Examine the output for:

SPI: ``` dtparam=spi=on ```

I2C: ``` dtparam=i2c_arm=on ```

1-Wire: ``` dtoverlay=w1-gpio ```


### Verify the hardware

1. To verify the model, run: ``` cat /sys/firmware/devicetree/base/model ```
2. To verify the OS, run: ``` lsb_release -a ```
3. To verify the memory, run: ``` free -h ```
4. To verify the disk free space, run: ``` df -h ``` 


### Generate an SSH key

1. Run: ``` ssh-keygen -t rsa ```
2. Use the default filename: Press Enter
3. Do not enter a passphrase: Press Enter
4. Do not re-enter the passphrase: Press Enter


### Install your computer's SSH key

1. ``` nano .ssh/authorized_keys ```

ssh-rsa AAAAB3...r0XdM= don@Donalds-MBP

2. Ctrl-O
3. Enter
4. Ctrl-X



### Install an I2C hardware clock

1 - 3.3V - Red

3 - SDA  - Blue

5 - SCL  - Yellow

9 - GND  - Black

STEMMA QT / Qwiic JST SH 4-pin Cable with Premium Female Sockets - 150mm Long

https://www.adafruit.com/product/4397

Adafruit DS3231 Precision RTC - STEMMA QT

https://www.adafruit.com/product/5188

STEMMA QT / Qwiic JST SH 4-pin to Premium Male Headers Cable - 150mm Long

https://www.adafruit.com/product/4209

CR1220 12mm Diameter - 3V Lithium Coin Cell Battery - CR1220

https://www.amazon.com/dp/B06XQ1C5TN

From Adafruit: https://learn.adafruit.com/adafruit-ds3231-precision-rtc-breakout

From: https://raspberry.tips/en/raspberrypi-tutorials/raspberry-pi-rtc-ds3231-setup

```
sudo apt install i2c-tools -y

sudo i2cdetect -y 1
# you should see 68

# modify the config
sudo nano /boot/firmware/config.txt

# Add the following for DS3231
dtoverlay=i2c-rtc,ds3231
```

Ctrl-O

Enter

Ctrl-X


```
sudo reboot
```

Log back into your RPi.

```
# remove fake-hwclock
sudo apt remove fake-hwclock -y

# install the hwclock program
sudo apt install util-linux-extra -y

# after rebooting, read the current time from the DS3231
sudo hwclock -r
# -OR-
timedatectl

# first check the system time. If it's not correct,
# use date to set the date and time manually.
date

# if the Pi has internet access, the system time is 
# already correct via NTP. Write it to the RTC module:
sudo hwclock -w

# verify
sudo hwclock -r
```


### Install an I2C soil sensor

1 - 3.3V - Red

3 - SDA  - Blue

5 - SCL  - Yellow

9 - GND  - Black

Adafruit STEMMA Soil Sensor - I2C Capacitive Moisture Sensor - JST PH 2mm

https://www.adafruit.com/product/4026

4-pin JST PH to JST SH Cable - STEMMA to QT / Qwiic - 200mm long

https://www.adafruit.com/product/4424

Additional cables as needed

https://www.adafruit.com/product/4399

20 Gauge 4 Conductor Electrical Wire 50FT, UL 2464 20 AWG 4 Wire Cable

https://www.amazon.com/dp/B0CN76MG6P

```
sudo i2cdetect -y 1
# you should see 36, or if you've soldered some address points: 37, 38, or 39
```

### Install a 1-Wire thermometer

4 - 5.0V  - Red

6 - GND   - Black

7 - GPIO4 - Brown

Waterproof 1-Wire DS18B20 Digital temperature sensor (No Pullup Resistor)

https://www.adafruit.com/product/381

-OR-

Weewooday 4 Sets Ds18b20 Temperature Sensor Module Kit with 1 M/ 3.2 ft (With Pullup Resistor)

https://www.amazon.com/dp/B0924NBNZP

Record it's serial number found in /sys/bus/w1/devices/

``` 
sudo modprobe w1-gpio
sudo modprobe w1-therm
ls -lap /sys/bus/w1/devices 
```

Label it.


### Install a relay hat

Header Pins

GeeekPi 4 Channel I2C Relay Board Module for Raspberry Pi, Power Relay Module for Raspberry Pi 4B/3B+/3/2B (No Programming Required/Programmable) 

https://www.amazon.com/dp/B07Q2P9D7K

Model EP-0099

1 - 3.3V - Red

3 - SDA  - Blue

5 - SCL  - Yellow

9 - GND  - Black

This relay hat has 4 mustard colored relays with green terminals on a black PCB board.

-OR-

Electronics-Salon RPi Power Relay Board Expansion Module for Raspberry Pi A+ 3A+ B+ 2B 3B 3B+ 4B

https://www.amazon.com/dp/B07CZL2SKN

Model D-1226H

 2 - 5.0V 

 4 - 5.0V

 6 - GND
 
 9 - GND
 
14 - GND

20 - GND

25 - GND

30 - GND

34 - GND

39 - GND

37 - GPIO26 - Relay 1

38 - GPIO20 - Relay 2

40 - GPIO21 - Relay 3

This relay hat has 3 black colored relays with green terminals on a green PCB board.

#### Example source
git@github.com:donaldbales/d-1226h.git


#### Additional Components

Sequent Microsystems Home Automation V4 8-Layer Stackable HAT for Raspberry Pi

https://www.amazon.com/Eight-RELAYS-8-Layer-Stackable-Raspberry/dp/B07KRKS67G


TWTADE/JQX-12F-2Z DC 12V Coil Voltage 30A DPDT 2NO+2NC General Purpose High Power Relay 8 Pin

https://www.amazon.com/dp/B07FCL6MQY


U.S. Solid NPT Brass Electric Solenoid Valve 12V DC Normally Closed VITON (3/4 inch) 

https://www.amazon.com/dp/B00DQ1J4H0


### Python Resources

https://www.python.org/

https://docs.python.org/3/

https://docs.python.org/3/builtins/index.html

https://docs.python.org/3/library/index.html

https://devguide.python.org/

https://docs.circuitpython.org/en/latest/README.html

https://assets.openstax.org/oscms-prodcms/media/documents/Introduction_to_Python_Programming-WEB.pdf

Since the Raspi O.S. has a managed version of Python, you need to create a virtual Python environment in your home directory

```
cd ~
python3 -m venv mypy
```
That command copied the managed environment Python to your ~/mypy directory located in you home directory.

Edit your .profile adding the following line to put the ``` mypy ``` virtual environment in your path.
```
nano .profile

# scroll to the end of the file and add:
PATH="$HOME/mypy/bin:$PATH"
```
Ctrl-O

Enter

Ctrl-X


### Git 

Commands
```
git clone \<git repo url> 
```

```
git add .
git commit -m "This is why"
git push
```

```
git pull
```


### Create a program to read the soil sensor


https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor


#### Example Source

Install the driver software.
```
pip3 install adafruit-circuitpython-seesaw
```

https://github.com/donaldbales/cap-moist-sens

```
git clone https://github.com/donaldbales/cap-moist-sens.git
```

### Create a program to read the 1-Wire thermometer

https://www.digikey.com/en/articles/how-to-efficiently-connect-to-sensors-in-iot-endpoints-using-1-wire-communication

#### Example Source

https://github.com/donaldbales/ds18b20

```
git clone https://github.com/donaldbales/ds18b20.git
```


### Create a program to turn relays on and off

#### Example Source

https://github.com/donaldbales/d-1226h

```
git clone https://github.com/donaldbales/d-1226h.git
```

-OR-

Install the driver software.
```
pip3 install smbus
```

https://github.com/donaldbales/ep-0099

```
git clone https://github.com/donaldbales/ep-0099.git
```

### Create a data collection program

https://github.com/donaldbales/garden

data_logger.py

```
git clone https://github.com/donaldbales/garden.git
```


Create a data transmission program

https://github.com/donaldbales/garden

data_sender.py

```
git clone https://github.com/donaldbales/garden.git
```


### Set email password in root environment

1. ``` sudo nano /etc/bash.bashrc ```

```
# System-wide .bashrc file for interactive bash(1) shells.

export EMAIL_PASSWORD='My Email Password'

...
```
2. Ctrl-O
3. Enter
4. Ctrl-X


### Create a daemon configuration file

```
sudo systemctl edit --force --full <daemon name>
```

```
[Unit]
Description=<daemon name>
[Service]
Environment="EMAIL_PASSWORD=<password>"
Type=Simple
RestartSec=30
User=don
StandardOutput=append:/home/don/compost/data_logger.log
StandardError=append:/home/don/compost/data_logger.err
ExecStart=/home/don/compost/data_logger.py
WorkingDirectory=/home/don/compost
[Install]
WantedBy=multi-user.target
```


### Start the daemon

```
sudo systemctl start <daemon name>
```

### Restart the daemon

```
sudo systemctl restart <daemon name>
```


### Set the daemon to autostart on boot

```
sudo systemctl enable <daemon name>
```


### Stop the daemon

```
sudo systemctl stop <daemon name>
```


### Check the daemon status

```
sudo systemctl status <daemon name>
```

-OR-

```
ps -Al | grep -v grep | grep <daemon name>
```

-OR-
```
top
```
press L daemon name


### Backup

Make sure you have a back plan in place.


### Data Receiver

#### Example Source

https://github.com/donaldbales/node-garden-receiver

```
git clone https://github.com/donaldbales/node-garden-receiver.git
```

## Feedback

#### Send Feedback To

Donald Bales

don@donaldbales.com

