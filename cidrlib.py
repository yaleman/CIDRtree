#cidrlib.py
import re
import os, sys

from bitstring import Bits # https://pythonhosted.org/bitstring/creation.html


CIDRVALIDATE = re.compile( "^(?P<address>[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})\/(?P<mask>[\d]{1,2})$" )

class CIDRfile:
	def __init__( self, filename ):
		self.filecontents = self.getfile( filename )

	def getfile( self, filename ):
		""" gets the contents of a file, returns False if it doesn't exist or isn't actually a file """
		if( os.path.exists( filename ) and os.path.isfile( filename ) ):
			# TODO: deal with unable to open file errors etc
			fh = open( filename, 'r' )
			return fh.read().strip()
		else:
			return None

	def cleanfile( self, filestring ):
		""" cleans not-allowed details, may return a report """
		filestring = filestring.replace( "\r\n", "\n" )

		#TODO: replace the below with a regex for whitespace
		filestring = filestring.replace( "\t", " " ) 		# replace tabs with spaces
		while "  " in filestring: 							# replace doublespaces
			filestring = filestring.replace( "  ", " " )
		return filestring

	def fileprocess( self, filestring ):
		""" deals with a file full of host definitions,
			turns it to an array full of tuples of name/CIDR """
		filestring = self.cleanfile( filestring )
		lines = filestring.split( "\n" )
		data = []
		for line in lines:
			if( line.strip() != "" ):		# ignore empty lines
				site, net = line.split()
				net, mask = net.split( '/' )
				data.append( ( net.strip(), int( mask ), site.strip() ) )
		return data

	def makecidrs( self, cleanfile ):
		""" takes the output from fileprocess() and returns a list of CIDR objects """
		cidrs = []
		for entry in cleanfile:
			net, mask, name = entry
			cidrs.append( CIDR( "{}/{}".format( net, mask ), name ) )
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
			self.address = tmp.group( 1 ) # TODO: this needs to be private and have a setter function)
			self.mask = int( tmp.group( 2 ) ) # TODO: this needs to be private and have a setter function)
			if self.mask >32 or self.mask < 0:
				raise TypeError( "Bitmask is wrong: '{}'".format( str( self.mask ) ) )
			tmp = False

			self.name = name
			self.children = []			# store children

			self.binarynetmask = Bits( bin=( "1" * self.mask) + ( ( 32 - self.mask ) * "0" ) ) # binary netmask
			self.binaryaddress = Bits( uint=self.iptoint( self.address ), length=32 ) # binary version of address

	def __str__( self ):
		return "{} {}/{}".format( self.name, self.address, self.mask)

	def getmask( self ):
		""" returns the CIDR mask, it's an int """
		return self.mask

	def getaddress( self ):
		""" returns the address, a string """
		return self.address

	def getname( self ):
		""" returns the string name of the CIDR """
		return self.name

	def iptoint( self, address ):
		""" takes an ip address in string form and turns it to an integer
		pass str( address )
		returns false if it's an invalid string
		"""
		a,b,c,d = address.split( "." )
		intval = ( int( a ) * ( 256 ** 3 ) ) + ( int( b ) * ( 256 ** 2 ) ) + ( int( c ) * 256 ) + int( d )
		return int( intval )




	def haschildren( self ):
		""" checks if this CIDR has children """
		return len( self.children ) > 0

	def cancontain( self, cidrclass ):
		""" checks if a given CIDR object can be contained within this one """
		if( cidrclass.getmask() > self.mask ): # smaller mask, that's a start
			if( ( cidrclass.binaryaddress & self.binarynetmask ) == self.binaryaddress ): # do some binary math
				return True
		return False

	def addchild( self, cidrclass ):
		""" adds a given CIDR object as a child, but checks children to see if it's
		 better placed lower on the tree
		returns True if successful, False if not """
		if( self.cancontain( cidrclass ) ): 					# check if it's possible to fit
			if( self.haschildren() ):							# check if can be placed lower
				for child in self.children:
					if child.addchild( cidrclass ) == True:		# it's recursive!
						return True								# break out of loop
			self.children.append( cidrclass ) 					# falls through to adding as a child
			return True
		else:
			return False
