#!/usr/bin/env python
# process.py

# Author: Francis M. Columbus
# Purpose:
# This program uses software timed loops to cycle an AC load ON / OFF for a specified 
# number of cycles with a preset ON duration in minutes and a preset OFF duration.
# If zero is specified for the number of cycles, the loop is continuous.
# The hardware of the Raspberry Pi is augmented with the PiFace Relay / Switch module.
#
# This program is designed for Python 2.x. Here is an example of one of the differences:
# If you do not use the 'raw_input' command, the 'input' command tries to interpret the string as a command unless the value is numeric.
# except Python v3.3 does not behave as above - use the simple 'input'.
#
#   Version 1.20 
#   December 3, 2013

import sys
import go
import time
oldstdout = sys.stdout	# Save the initial state of standard output

def iterations (cycles):
        """ 
            This function gets the number of times the user wants to run an "ON" / "OFF" Cycle of the powered machinery.
            If the user enters "0", it is interpreted as a code for run continuous.
            To halt the system, 4 basic methods are available short of a hard reset:
            1) Enter Control C, 
            2) Press the stop button on the PiFace module,
            3) Execute "python stop.py" locally,
            4) Execute "python stop.py" via Twitter using the "rpitwit" middleware.
            If the user enters a negative number the application flags an error and the user is prompted again.
        """

        cycles = 0
        while True:
                    try:    
                        cycles = int(raw_input('\n\nHow many process cycles would you like? Zero means continuous. '))          
                        return abs(cycles)
                    except ValueError:
                        print('\nPlease enter 0 or a positive integer value.\n')

def active ():
        """ 
            This function prompts the user for the time the controlled machinery is in the "ON" state.
            The application prompt first for the magnitude and then for the units.
            Lower case "m" for minutes or lower case "s" for seconds.
            If the user enters a negative number the application flags an error and the user is prompted again.
        """
  
        on = 0
	units = 'a'
        unit_mult_on = 1
        valid_input = False
        while not valid_input:
                    try:
                         while (on == 0):
                             on = int(raw_input('\nHow long do you want the system on (magnitude first then units)? '))
                             if (on < 0):
                                 on = 0
                                 print('\nPlease enter a positive integer value.\n')
                             else:
                                 valid_input = True
                    except ValueError:
                         print('\nPlease enter a positive integer value.\n')
        valid_input = False                    
        while (units != 'm' and units != 's' and valid_input is False):
                    units = str(raw_input('\nEnter lower case \'s\' for seconds or lower case \'m\' for minutes: '))
                    if (units == 's'):
                         unit_mult_on = 1
                         valid_input = True
                    if (units == 'm'):
                         unit_mult_on = 60
                         valid_input = True
        return (abs(on), int (unit_mult_on))


def inactive ():
        """ 
            This function prompts the user for the time the controlled machinery is in the "OFF" state.
            The application promptt first for the magnitude and then for the units.
            Lower case "m" for minutes or lower case "s" for seconds.
            If the user enters a negative number the application flags an error and the user is prompted again.
        """

        off = 0
	units = 'a'
        unit_mult_off = 1
        valid_input = False
        while not valid_input:
                    try:
                        while (off == 0):
                         off = int(raw_input('\nHow long do you want the system off (magnitude first then units)? '))
                         if (off < 0):
                             off = 0
                             print('\nPlease enter a positive integer value.\n')
                         else:
                             valid_input = True
                    except ValueError:
                        print('\nPlease enter a positive integer value.\n')
        valid_input = False
        while (units != 'm' and units != 's'):
                    units = str(raw_input('\nEnter lower case \'s\' for seconds or lower case \'m\' for minutes: '))
                    if (units == 's'):
                         unit_mult_off = 1
                         valid_input = True
                    if (units == 'm'):
                         unit_mult_off = 60
                         valid_input = True
        return (abs(off), int (unit_mult_off))
                    

def process (cycles, on, unit_mult_on, off, unit_mult_off):
        """ 
            This function contains the actual timing loops and calls to the PiFace firmware.
            It will let the user know how many cycles have been completed by sending an update to the console.
            This function also monitors the contents of "control.txt". Please refer to the doc string in main 
            for details on the operation using "control.txt".
            If a pause of the cycle is invoked locally or via Twitter.com, a counter-clockwise rotating 
            character icon is output to the console.
        """

        from time import sleep
        import piface.pfio as pfio
        pfio.init( )
        controlString = ''
        if cycles > 0:
            count = 1
            for count in range (1, cycles + 1):
                pfio.digital_write(0,1)     # Turn relay 0 / LED 0 ON
                sleep(on * unit_mult_on)     
                                           
                pfio.digital_write(0,0)     # Turn relay 0 / LED 0 OFF
                                            
                sleep(off * unit_mult_off)
                print ('Cycles completed: '+ str(count))
                controlString = str(readFile('control.txt'))
                if controlString == 'STOP':
                    exit (0)
		if controlString == 'PAUSE':
                    print ('Waiting...')
                while controlString == 'PAUSE':
	            sigwait()
                    controlString = str(readFile('control.txt'))

            return
        else:
            count = 0
            while (True):           
                pfio.digital_write(0,1)     # Turn relay 0 / LED 0 ON
                sleep(on * unit_mult_on)           
                                            
                pfio.digital_write(0,0)     # Turn relay 0 / LED 0 OFF
                                            
                sleep(off * unit_mult_off)
                count = count + 1
                print ('Cycles completed: '+ str(count))
                controlString = str(readFile('control.txt'))
                if controlString == 'STOP':
                    exit (0)
		if controlString == 'PAUSE':
                    print ('Waiting...')
                while controlString == 'PAUSE':
                    sigwait()	
                    controlString = str(readFile('control.txt'))
                   
        return

def sigwait():					
        """ 
            Create a delay but still output an indication to the console.
        """
 
	j = 0				
        print(' |\r'),
        print('  \r'),
        print(' /\r'),
        print('  \r'),
        print(' -\r'),
        print('  \r'),
        print(' \\ \r'),
        print('  \r'),
        while j < 5000:
            j = j + 1
        return

def readFile(fname):
        """ 
            This function reads a file and is used here to monitor the run state indicated by the contents 
            of "control.txt". See description in the doc string of function main for details.
        """

	fn = open(fname, 'r')
        controlString = str(fn.read())
	fn.close()
        return (controlString)

        
def main ( ):
        """ 
            In order to implement a feature for basic "Cloud Control" via Twitter.com, this program uses three small
            programs: go.py, stop.py, and wait.py. These programs write a single control word to a small text file.
            The words are: RUN, STOP, and PAUSE, respectively. The text file is "control.txt". This file is also 
            altered locally by invoking the control programs via the command line or via scanswitch.py, a program
            that monitors the PiFace push button switches. 
        """

        correct = 0
        cycles = 0
        on = 0
        off = 0
        test = 'n'
        unit_mult_on = 1
        unit_mult_off = 1

        go.goControl()                                         # Initialize "control.txt" to "RUN"


        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print('\n   FrankNet Automation Process Control\n\n')
        print('\nThis application allows you to cycle a machine')
        print('ON and OFF for a predefined number of cycles.\n')
        print('Alternatively, you may enter \'0\' for the number')
        print('of cycles to run continuously.\n')
        print('You specify the duty cycle in minutes or seconds that')
        print('the system will be ON and will be OFF.\n')
        print('Valid values are never negative!')
        print('\nFor each part of the cycle, you will be asked for the numerical value first')
        print('and then you will select the units by entering \"m\" or \"s\".\n')

        
        while correct ==0:
            cycles = iterations(cycles)
            on, unit_mult_on = active()
            off, unit_mult_off = inactive()
    
            if cycles == 0:
                print ('\nRun continuous')
                print('On  State= ' + str(on)),
                if (unit_mult_on == 1):
                    print('seconds')
                else:
                    print('minutes')
 
                print('Off State= ' + str(off)),
                if (unit_mult_off == 1):
                    print('seconds')
                else:
                    print('minutes')

            else:
                print('\nCycles= ' + str(cycles))
                print('On  State= ' + str(on)),
                if (unit_mult_on == 1):
                    print('seconds')
                else:
                    print('minutes')

                print('Off State= ' + str(off)),
                if (unit_mult_off == 1):
                    print('seconds')
                else:
                    print('minutes')
   

            test = raw_input('\nIs this correct (y/n)? ').strip()       
            
            if test == 'y' or test == 'Y' or test == 'yes' or test == 'Yes' or test == 'YES':
                correct = 1
        
        print('\n\nProcess starting...' )
 #       print(cycles, on, unit_mult_on, off, unit_mult_off )
        process (cycles, on, unit_mult_on, off, unit_mult_off)
        
main ( )
