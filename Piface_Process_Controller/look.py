#!/usr/bin/env python
# look.py

# Author: Francis M. Columbus
# Purpose:
# Diagnostic test file for repeatedly reading control.txt

#   Version 1.2
#   December 3, 2013

def readFile(fname):
        """ 
           Read and print the contents of 'control.txt
           to stdout.
        """

	fn = open(fname, 'r')
	print (fn.read())
	fn.close()
        return 
	
def main():
    loopctl = True
    while loopctl is True:
	control_word = str(readFile('control.txt'))
        print control_word[:0]       # Printing the [:0] value of the array eliminates
	                             # the extraneous word "None" from the end of file.
main()