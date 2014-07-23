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

CIDRVALIDATE = re.compile( "^[\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}/[\d]{1,2}$" )

class CIDR( object ):
	""" CIDR definition """

	def init( self, CIDRstring ):
		""" feed it a CIDR x.x.x.x/y and it'll do things. """
		if not CIDRVALIDATE.match( CIDRstring ):
			
			return False
