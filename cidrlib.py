#cidrlib.py
import re
import os, sys

from bitstring import BitArray, BitStream, Bits


CIDRVALIDATE = re.compile( "^(?P<address>[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})\/(?P<mask>[\d]{1,2})$" )


def getfile( filename ):
	""" gets the contents of a file, returns False if it doesn't exist or isn't actually a file """
	if( os.path.exists( filename ) and os.path.isfile( filename ) ):
		# TODO: deal with unable to open file errors etc
		fh = open( filename, 'r' )
		return fh.read()
	else:
		return None

def cleanfile( filestring ):
	""" cleans not-allowed details, may return a report """
	# replace tabs with spaces
	filestring = filestring.replace( "\t", " " )
	filestring = filestring.replace( "\r\n", "\n" )
	# replace doublespaces
	while "  " in filestring:
		filestring = filestring.replace( "  ", " " )
	return filestring

def fileprocess( filestring ):
	""" deals with a file full of host definitions,
		turns it to an array full of tuples of name/CIDR """
	filestring = cleanfile( filestring )
	lines = filestring.split( "\n" )
	data = []
	for line in lines:
		if( line.strip() != "" ):		# ignore empty lines
			site, net = line.split()
			data.append( ( net.strip(), site.strip() ) )
	return data

def makecidrs( cleanfile ):
	""" takes the output from fileprocess() and returns a list of CIDR objects """
	cidrs = []
	for entry in cleanfile:
		net, name = entry
		cidrs.append( CIDR( net, name ) )
	return cidrs

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
			if self.mask >32 or self.mask < 0:
				raise TypeError( "Bitmask is wrong: '{}'".format( str( self.mask ) ) )
			tmp = False

			self.name = name
			self.children = []			# store children

	def __str__( self ):
		return "{} {}/{}".format( self.name, self.address, self.mask)

	def getmask( self ):
		return self.mask

	def getaddress( self ):
		return self.address

	def getname( self ):
		return self.name

	def cancontain( self, cidrclass ):
		if( cidrclass.getmask() < self.mask ):
			# smaller mask, that's a start
			return True

	def iptoint( self, address ):
		""" takes an ip address in string form and turns it to an integer
		pass str( address )
		returns false if it's an invalid string
		"""
		a,b,c,d = address.split( "." )
		intval = ( int( a ) * ( 256 ** 3 ) ) + ( int( b ) * ( 256 ** 2 ) ) + ( int( c ) * 256 ) + int( d )
		print( "{} {} {}".format( address, intval, type( intval ) ) )
		return int( intval )

	def binary_netmask( self, reset=False ):
		return BitArray( bin=( "1" * self.mask) + ( ( 32 - self.mask ) * "0" ) )
