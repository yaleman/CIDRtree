#!/usr/bin/python

""" takes some flat files with host group definitions and does things. this description will get better!
"""

from re import compile

def getfile( filename ):
	""" gets the contents of a file """
	return False

def csvprocess( csvstring ):
	""" deals with a csv string """
	return False

def cleanfile( filestring ):
	""" cleans not-allowed details, may return a report """
	return False

CIDRVALIDATE = compile( "^[\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}/[\d]{1,2}$" )

def log( logstring ):
	""" log something, currently goes to console """
	print( "{}".format( logstring ) )
	return True

class CIDR:
	""" CIDR definition """
	def __init__( self, CIDRstring ):
		""" feed it a CIDR x.x.x.x/y and it'll do things. """
		if not CIDRVALIDATE.match( CIDRstring ):
			raise TypeError( "{} isn't a valid CIDR?".format( CIDRstring ) )
		else:
			

test = CIDR( "10.0.0.4/8" )
try:
	test = CIDR( "10.0.0.0" )
except TypeError:
	log( "Testing: This should error, as it's not a valid CIDR" )
