from cidrtree import *

def test_cidrvalidate():
	""" Testing the CIDRVALIDATE regex. """
	teststring = "192.1.2.234/32"
	ts_test = CIDRVALIDATE.match( teststring )
	assert ts_test.group( 0 ) == "192.1.2.234/32"
	assert ts_test.group( 1 ) == "192.1.2.234"
	assert ts_test.group( 2 ) == "32"
	teststring = "2.3.4.5"
	ts_test = CIDRVALIDATE.match( teststring )
	assert ts_test == None

def test_getfile():
	""" Testing getfile() """
	assert getfile( "./testdata/singlevalidCIDR.txt" ), "10.0.0.0/24"

def test_fileprocess():
	""" Testing fileprocess() """
	assert fileprocess( "site 	 10.0.0.0/24"), [ ("site", "10.0.0.0/24" ) ]

def test_CIDR_stringret():
	""" Testing the string return for the CIDR class """
	tmp = CIDR( "10.0.0.8/8", "butts" )
	assert str( tmp ), "butts 10.0.0.8/8"

try:
	test = CIDR( "10.0.0.0" )
except TypeError:
	pass
