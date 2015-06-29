#!/usr/bin/env python
# scanswitch.py
 

# Author: Francis M. Columbus
# Purpose:
# This control script writes the word "RUN", "PAUSE", or "STOP" to "control.txt".
# This module will overwrite any prior value in control.txt
#
#   Version 1.2
#   December 3, 2013

import time

def goControl():
    """ 
       This function writes the word "RUN" to "control.txt".
    """
    f = open('control.txt', 'w')
    f.write('RUN')
    f.close()

def waitControl():
    """ 
       This function writes the word "PAUSE" to "control.txt".
    """
    f = open('control.txt', 'w')
    f.write('PAUSE')
    f.close()

def stopControl():
    """ 
       This function writes the word "STOP" to "control.txt".
    """
    f = open('control.txt', 'w')
    f.write('STOP')
    f.close()

def scanSwitch():
    import piface.pfio as pfio
    pfio.init() 
    loopctl = True
    button1 = 0
    button2 = 0
    button3 = 0
    button4 = 0
    input6 = 0                             # input6 and input7 are 5V logic level control signals from Arduino.
    input7 = 0
    goControl()                       
    while loopctl is True:

        for i in range (1, 15000):             # These loops indexed by "i" are delay loops to reduce keybounce.
	    delay = 0
        button1 = int(pfio.digital_read(0))    # Read the outer most button
        if button1 == 1:
            print('Stop button pressed')
            stopControl()
            for i in range (1, 15000):
		delay = 0

        button2 = int(pfio.digital_read(1))     # Read the second middle button 
        if button2 == 1:
            waitControl()
            print('Pause button pressed')
            for i in range (1, 1500):
                delay = 0   
 
        button3 = int(pfio.digital_read(2))     # Read the first middle button
        if button3 == 1:
            waitControl()
            print('Pause button pressed')
            for i in range (1, 15000):
		delay = 0

        button4 = int(pfio.digital_read(3))    # Read the inner most button
        if button4 == 1:
            goControl()
            print('Go button pressed')
            for i in range (1, 15000):
		delay = 0
		
        input6 = int(pfio.digital_read(6))    # Read the digital input pin 6, PAUSE signal from Arduino.
        input7 = int(pfio.digital_read(7))    # Read the digital input pin 7, GO signal from Arduino.
        if input6 == 1 and input7 == 0:       # PAUSE when true
           for i in range (1, 5000):
               delay = 0
           if input6 == 1 and input7 == 0:
               waitControl()
               print('WAIT signal from Arduino')   # Suppress multiple triggers

        if input6 ==0 and input7 == 1:        # GO when true
           for i in range (1, 5000):
               delay = 0
           if input6 == 0 and input7 == 1:
               goControl()
               print('GO signal from Arduino')   # Suppress multiple triggers
         

def main():
    scanSwitch()

main()
