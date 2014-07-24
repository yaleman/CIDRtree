#!/usr/bin/python

""" takes some flat files with host group definitions and does things. this description will get better!
"""

from re import compile
import os
import sys

CIDRVALIDATE = compile( "^(?P<address>[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})\/(?P<mask>[\d]{1,2})$" )


def getfile( filename ):
	""" gets the contents of a file, returns False if it doesn't exist or isn't actually a file """
	if( os.path.exists( filename ) ):
		if( os.path.isfile( filename ) ):
			fh = open( filename, 'r' )
			return fh.read()
			# TODO: deal with unable to open file errors etc
	return False


def fileprocess( filestring ):
	""" deals with a file full of host definitions,
		turns it to an array full of tuples of name/CIDR """
	filestring = cleanfile( filestring )
	lines = filestring.split( "\n" )
	data = []
	for line in lines:
		if( line.strip() != "" ):		# ignore empty lines
			site, net = line.split()
			data.append( ( site.strip(), net.strip() ) )
	return data


def cleanfile( filestring ):
	""" cleans not-allowed details, may return a report """
	# replace tabs with spaces
	filestring = filestring.replace( "\t", " " )
	filestring = filestring.replace( "\r\n", "\n" )
	# replace doublespaces
	while "  " in filestring:
		filestring = filestring.replace( "  ", " " )
	return filestring

def log( logstring ):
	""" log something, currently goes to console """
	print( "{}".format( logstring ) )
	return True

class CIDR:
	""" CIDR definition """
	def __init__( self, CIDRstring, name ):
		""" feed it a CIDR x.x.x.x/y and it'll do things. """
		if not CIDRVALIDATE.match( CIDRstring ):
			raise TypeError( "{} isn't a valid CIDR?".format( CIDRstring ) )
		else:
			# break down the CIDR
			tmp = CIDRVALIDATE.match( CIDRstring )
			self.address = tmp.group( 1 )
			self.mask = int( tmp.group( 2 ) )
			tmp = False

			self.name = name
			self.children = []			# store children

	def __str__( self ):
		return "{} {}/{}".format( self.name, self.address, self.mask)

if __name__ == "__main__":
	print( "Hello user" )

	if len( sys.argv ) > 1:
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
