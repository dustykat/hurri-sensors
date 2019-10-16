#!/usr/bin/env python
# Code to record Hall Detector events and coonvert into flow rate
# by T.G. Cleveland 
# Base Code from : https://raspberrypi.stackexchange.com/questions/34480
#
# Tested (no sensor) 6 FEB 2019 - exit keybopard OK
#                               - syntax check OK
#
import RPi.GPIO as GPIO
import time,sys
# set sensor pin
flow_sensor = 23 
#
# configure GPIO 
GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_sensor, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#
# initialize counter(s)
#
global count
count = 0
#
# define a counter method
#
def countPulse(channel):
   global count
   if start_counter == 1:
      count = count + 1
#   now = time.strftime("%c") # capture actual time as center of sampling interval
#   print count
#   flow = count / (60.0 * 7.5) # force to float 
#   print(now + ' ' + str(count) + ' ' + str(flow))
#   print(now)
#
# 
GPIO.add_event_detect(flow_sensor, GPIO.FALLING, callback=countPulse)

while True:
   try:
      start_counter = 1
      time.sleep(1)
      start_counter = 0
      flow = (count * 60 * 2.25 / 1000)
      now = time.strftime("%c") # capture system time
      print(now + '  Events = ' + str(count) + '  L/min = ' + str(flow))
      count = 0
      time.sleep(4)
   except KeyboardInterrupt:
      print '\ncaught keyboard interrupt!, bye'
      GPIO.cleanup()
      sys.exit()

