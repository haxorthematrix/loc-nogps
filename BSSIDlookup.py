#!/usr/bin/python
############################################################################
#                                                                          #
#  Name: Geolocate BSSIDs using Google                                     #
#                                                                          #
#  Description: BSSIDlookup accepts one input to the command line          #
#               and utilizes the iSniff GPS/undocumented API call to       #
#               determine location of APs                                  #
#                                                                          #
#  Usage: ./BSSIDlookup.py <colon separated BSSID>                         #
#                                                                          #
#  Requirements: Python                                                    #
#                python-netaddr                                            #
#                python-requests                                           #
#                BeautifulSoup                                             #
#                bs4                                                       #
#                pygmaps                                                   #
#                ElementTree                                               #
#                iSniffGPS wloc (included)                                 #
#                protobuf                                                  #
#                                                                          #
#  Authors: Larry Pesce - larry@inguardians.com @haxorthematrix            #
#           Don Weber - don@inguardians.com @cutaway                       #
#                                                                          #
#  Credits: * Nathan Sweaney - nathan@sweaney.com, for his work on KLV     #
#           where some of this code was adapted from/inspired by.          #
#           * Secure Ideas - RE: Nathan Sweaney                            #
#           * @hubert3 - hubert(at)pentest.com, for his hard work on       #
#           iSniffGPS, as this project would not be possible without it.   #
#           * Francois-Xavier Aguessy and Come Demoustier - For their work #
#           in the undocumented Apple API call for geolocation.            #
#           * @cutaway - for being a great friend, co-worker, and          #
#           instructing this python n00b in the ways of the force.         #
#           * InGuardians - for giving me a chance, and the honor of       #
#           working with and for my heroes.                                #
#           * @edwardmccabe and anonymous donors for sample files!         #
#                                                                          #
#  Date: September 19, 2014                                                #
#                                                                          #
############################################################################
from datetime import datetime
#from models import *
from string import lower
#import wigle
import wloc
import re
import sys
from netaddr import EUI

def AppleWloc(bssid=None):	
	#if not bssid:
	#	bssid = 'B8:C7:5D:09:AF:13'
	print 'Got request for %s' % bssid
	template='apple-wloc.html'
	#request.session['apdict'] = {}
	#request.session['apset'] = set() #reset server-side cache of unique bssids if we load page normally
	#print '%s in set at start' % len(request.session['apset'])
	bssid=lower(bssid)
	apdict = wloc.QueryBSSID(bssid)	
	print '%s returned from Apple' % len(apdict)
	for key,value in apdict.items():
		#print "Key:",key," - sys.argv[1]:",sys.argv[1].lower()
		if key == str(sys.argv[1].lower()):
			print key,":", value

AppleWloc(str(sys.argv[1]))
