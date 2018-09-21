#!/usr/bin/env python

import json
import urllib
import os
import subprocess
from subprocess import call
import pyping
import math
import random

home_location = {
	'lat' : 49.062559,
	'long' : -122.820597
}

NORDVPN_SERVER_URL='https://nordvpn.com/api/server'

def get_ping( server ):
	r = pyping.ping( server )
	return float( r.avg_rtt )

def geo_distance( location ) :
	d_lat = math.pow( home_location[ 'lat' ] - location[ 'lat' ], 2 )
	d_long = math.pow( home_location[ 'long' ] - location[ 'long' ], 2 )
	return math.sqrt( d_lat + d_long )

def server_select( servers ):
	random.seed()
	candidates = []
	for s in servers:
		if s[ 'flag' ] == 'CA' and 'P2P' in s[ 'search_keywords' ]:
			candidates.append( s )

	for c in candidates:
		c[ 'geo_location' ] = geo_distance( c[ 'location' ] )
	candidates.sort( key=lambda x: x[ 'geo_location' ] )

	n_candidates = random.randrange( 5, 10 )

	print 'picking closest', n_candidates, ' to home location'

	candidates = candidates[ 1 : n_candidates + 1 ]

	for c in candidates:
		print 'pinging server', c[ 'domain' ]
		c[ 'ping' ] = get_ping( c[ 'domain' ] )
		c[ 'score' ] = c[ 'ping' ] + c[ 'load' ]

	candidates.sort( key=lambda x: x[ 'score' ] )


	print 'showing server ranking'
	print "server ping load"
	for c in candidates:
		print c[ 'domain' ], c[ 'ping' ], c[ 'load' ]

	return candidates[ 0 ]

def server_connect( server ):
	print 'connecting to', server
	call( [ "openvpn",
			'/etc/openvpn/ovpn_tcp/' + server + '.tcp.ovpn'
		  ] )

if __name__ == '__main__':
	if os.getuid() != 0:
		print "run as root!"
		exit( 0 )
	response = urllib.urlopen( NORDVPN_SERVER_URL )
	print response
	data = json.loads( response.read() )
	s = server_select( data )
	domain = s[ 'domain' ]
	server_connect( domain )
