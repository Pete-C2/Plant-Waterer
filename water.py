"""Plant Auto Waterer
Reads the configuration from an associated xml file.
Presents a set of webpages to display the control.
Controls the operation of a pump on a fixed schedule.
"""

from flask import Flask, render_template, request
import datetime
import xml.etree.ElementTree as ET
import os
import threading
import time
import csv
import RPi.GPIO as GPIO

# Pump control code: Turn the pump on at the scheduled time for the defined number of minutes.

class PumpThread ( threading.Thread ):

     def run ( self ):
          global control_interval
          global pump_state
          global log_on
          global log_off
          
          GPIO.setmode(GPIO.BOARD)
          print "Starting pump thread"

          for pump_pin in pump_pins:
               GPIO.setup(pump_pin, GPIO.OUT)
               GPIO.output(pump_pin, GPIO.LOW)

          try:
               while 1: # Control the pump

                    now = datetime.datetime.now().time()
                    
                    for count in pump_schedule:
                         if ((now >= pump_schedule[count]['time-on']) and (now < pump_schedule[count]['time-off'])):
                              for pump_pin in pump_pins:
                                   GPIO.output(pump_pin, GPIO.HIGH)
                                   pump_state = "On"
                                   print "Pumps on"
                         else:
                              for pump_pin in pump_pins:
                                   GPIO.output(pump_pin, GPIO.LOW)
                                   pump_state = "Off"
                                   print "Pumps off"
                   
                    time.sleep(control_interval)

          except KeyboardInterrupt:
               GPIO.cleanup()

app = Flask(__name__)

# Initialisation

pump_state = "Off"

# Read config from xml file

# Find directory of the program
dir = os.path.dirname(os.path.abspath(__file__))
# Get the configuration
tree = ET.parse(dir+'/config.xml')
root = tree.getroot()
pumps = root.find('PUMP')
display = root.find('DISPLAY')
water = root.find('WATER')

# Read hardware configuration
pump_pins = []
for child in pumps:
     pump_pins.append(int(child.find('RELAY').text))

# Read display settings configuration
title = display.find('TITLE').text

pump_names = []
for child in pumps:
     pump_names.append(child.find('NAME').text)
     

# Read time schedules
pump_schedule = {}
count = 1
for child in water:
     temp_on = datetime.datetime.strptime(child.find('TIME_ON').text, "%H:%M")
     temp_off = datetime.datetime.strptime(child.find('TIME_OFF').text, "%H:%M")
     schedule_time_on = temp_on.time()
     schedule_time_off = temp_off.time()
     pump_schedule[count] = {'time-on' : schedule_time_on, 'time-off' : schedule_time_off}
     print "Pump: " + str(count) + ". On at " + str(schedule_time_on) + " & off at " + str(schedule_time_off)
     count = count + 1


# Control
control_interval = 10 # seconds. Interval between control measurements

PumpThread().start()

# Flask web page code

@app.route('/')
def index():
     global title
     global log_status
     global pending_note
     now = datetime.datetime.now()
     timeString = now.strftime("%H:%M on %d-%m-%Y")

     templateData = {
                     'title' : title,
                     'time': timeString,
                     'pump' : pump_state,
                    }
     return render_template('main.html', **templateData)
 
@app.route('/confirm')
def confirm():
     templateData = {
                'title' : title
                }
     return render_template('confirm.html', **templateData)

@app.route('/shutdown')
def shutdown():
     command = "/usr/bin/sudo /sbin/shutdown +1"
     import subprocess
     process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
     output = process.communicate()[0]
     print output
     templateData = {
                'title' : title
                }
     return render_template('shutdown.html', **templateData)

@app.route('/cancel')
def cancel():
     command = "/usr/bin/sudo /sbin/shutdown -c"
     import subprocess
     process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
     output = process.communicate()[0]
     print output

     return index()


if __name__ == '__main__':
     app.run(debug=False, host='0.0.0.0')
     
     
