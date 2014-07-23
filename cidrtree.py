#!/usr/bin/python

""" takes some flat files with host group definitions and does things. this description will get better!
"""

from re import compile
import os

CIDRVALIDATE = compile( "^(?P<address>[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})\/(?P<mask>[\d]{1,2})$" )

def getfile( filename ):
	""" gets the contents of a file, returns False if it doesn't exist or isn't actually a file """
	if( os.path.exists( filename ) ):
		if( os.path.isfile( filename ) ):
			fh = open( filename, 'r' )
			return fh.read()
			# TODO: deal with unable to open file errors etc
	return False

def test_getfile():
	assert getfile( "./testdata/singlevalidCIDR.txt" ), "10.0.0.0/24"
	assert getfile( "./testdata/" ), False

def csvprocess( csvstring ):
	""" deals with a csv string """
	return False

def cleanfile( filestring ):
	""" cleans not-allowed details, may return a report """
	return False

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
			tmp = CIDRVALIDATE.match( CIDRstring )
			self.address = tmp.group( 1 )
			self.mask = tmp.group( 2 )
			tmp = False
			self.children = []

test = CIDR( "10.0.0.4/8" )
try:
	test = CIDR( "10.0.0.0" )
except TypeError:
	log( "Testing: This should error, as it's not a valid CIDR" )
