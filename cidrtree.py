#!/usr/bin/python

""" takes some flat files with host group definitions and does things. this description will get better!
"""


import os
import sys

from cidrlib import *


def main():
	""" main loop, need to write a test for this somehow """
	numargs = len( sys.argv )
	if( numargs == 1 ):
		print "Usage string should be here"
		return 1
	elif len( sys.argv ) > 2:
		print "Too many arguments, one file at a time bucko!"
		return 1
	else:
		# There's files.
		files = sys.argv[1:]
		openfiles = []
		for filename in files:
			filecontents = getfile( filename )
			if( filecontents != False ):
				filecontents =  cleanfile( filecontents )
				filecontents = fileprocess( filecontents )
				openfiles.append( ( filename, filecontents ) )
		print openfiles
		return 0


if __name__ == "__main__":
	""" main program flow """
	main()
