#!/usr/bin/env python
# wait.py

# Author: Francis M. Columbus
# Purpose:
# This control script writes the word "PAUSE" to "control.txt".
# This file is part of the Cloud Control package for process.py 
# and is called by "rpitwit" the open source twitter utility.
# to invoke a pause in the process, post "#rpitwit wait" to the user id
# that rpitwit is watching.
#
# ADDITIONAL NOTES:
# You must execute "rpitwit" from within the directory containing
# the Python scripts that you wish it to be able to call:
# for this system the path is: /home/pi/rpitwit_commands
#
# This module will overwrite any prior value in control.txt
#
#   Version 1.1 
#   December 3, 2013 

def waitControl():
    """ 
       This function writes the word "PAUSE" to "control.txt".
    """
    f = open('control.txt', 'w')
    f.write('PAUSE')
    f.close()

def main():
    waitControl()

main()

