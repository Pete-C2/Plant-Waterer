# Plant waterer
Plant auto waterer on a defined time schedule. Fixed on time at a fixed interval.

Requires:
- The [GPIO Library](https://code.google.com/p/raspberry-gpio-python/) (Already on most Raspberry Pi OS builds).
- The [Flask web server](https://www.raspberrypi.org/learning/python-web-server-with-flask/worksheet/). Install command:
  - sudo apt-get install python3-flask
- A [Raspberry Pi](http://www.raspberrypi.org/).
- Hardware to control a water pump.
- water pump!

Installation:
- Copy files to a folder on the Raspberry Pi.
- Edit /etc/rc.local to autorun application:
   - sudo nano /etc/rc.local
   - Add: python /home/pi/.../water.py where ... is the location of your file.
- Edit config.xml to define your system hardware. The defaults match my hardware.
    
Recommendations (to make life easier):
- Set a [static IP address](https://www.modmypi.com/blog/tutorial-how-to-give-your-raspberry-pi-a-static-ip-address).
- Define a [hostname](http://www.simonthepiman.com/how_to_rename_my_raspberry_pi.php).
- Create a [fileshare](http://raspberrypihq.com/how-to-share-a-folder-with-a-windows-computer-from-a-raspberry-pi/).
- Install [VNC](https://www.raspberrypi.org/documentation/remote-access/vnc/) for full headless access.

## Use

See wiki.

## Changelog

### V1.0
Fully working on a daily schedule to water plants

### V0.2
Working code controlling an LED.

### V0.1
Initial trial code.
