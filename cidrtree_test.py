import nose
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

def test_makecidrs():
	""" Testing makecidrs() """
	assert makecidrs( [("butts", "10.0.0.0/9")] ) == False

def test_CIDR_stringret():
	""" Testing the string return for the CIDR class """
	assert str( CIDR( "10.0.0.8/8", "butts" ) ), "butts 10.0.0.8/8"

def test_CIDR_regex():
	""" Testing the CIDR regex """
	nose.tools.assert_raises( TypeError, CIDR, "10.0.0.0", 'test' )

def test_CIDR_bitmaskchecker():
	""" Testing bitmask validation of CIDR class """
	nose.tools.assert_raises( TypeError, CIDR, "10.0.0.0/35", "test" )

def test_CIDR_getters():
	""" Testing CIDR get-functions """
	tmp = CIDR( "10.0.0.8/8", "butts" )
	assert tmp.getname(), "butts"
	assert tmp.getaddress(), "10.0.0.8"
	assert tmp.getmask(), 8
