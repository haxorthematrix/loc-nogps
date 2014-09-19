#!/usr/bin/python
############################################################################
#                                                                          #
#  Name: Geolocate multiple, unknown BSSIDs using Google                   #
#                                                                          #
#  Description: BSSIDlookup accepts one input to the command line          #
#               and utilizes the iSniff GPS/undocumented API call to       #
#               determine location of APs, while filling in for unknown    #
#               for up to 3 octets.                                        #
#                                                                          #
#  Usage: ./BSSIDbrute.py <colon separated BSSID>                          #
#         an "x" should represent the octets to bruteforce                 #
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
import sys
from netaddr import EUI

# Show status
STATUS = 0

# build possible values. These will be lower.
max_octet = 256
octets = [chr(x).encode('hex') for x in range(max_octet)]

def print_locs(networks):
    # Print networks and their location
    for key,value in networks.items():
        print key,":", value

def AppleWloc(bssid=None):
    # Query Apple for the bssid
    apdict = wloc.QueryBSSID(bssid.lower())
    # Print status if we are running large sets
    if STATUS: print ".",
    if STATUS: sys.stdout.flush()
    # Review returned values for the bssid
    networks = {key: value for key, value in apdict.items() if (key == bssid) and not (value[0] == -180.0)}
    # Return the values for the bssid
    return networks

# Generate possible networks
re_chr = 'x'
re_bssid = sys.argv[1].lower()
if not re_bssid.count(re_chr) or re_bssid.count(re_chr) > 3:
    print "Expected input 12:x:45:x:67:x with max of 3 x\'s"
    sys.exit()
# First run
tmp = [re_bssid.replace('x',x,1) for x in octets]
# Second run
if tmp[0].count('x'):
    tmp2 = []
    for e in tmp:
        tmp2.extend([e.replace('x',x,1) for x in octets])
    tmp = tmp2
# Third run
if tmp[0].count('x'):
    print "You know this is going to take FOREVER, right?"
    tmp2 = []
    for e in tmp:
        tmp2.extend([e.replace('x',x,1) for x in octets])
    tmp = tmp2

# Search for networks
# How to concantenate dictionaries. Not very efficient but easy: 'd4 = {}' 'for d in (d1, d2, d3): d4.update(d)'
#networks = {}
for e in tmp:

    # Process each bssid
    network = AppleWloc(bssid=e)

    # Store multiple networks together for future processing
    #networks.update(network)

    # Print results
    #print_locs(AppleWloc(bssid=e))
    print_locs(network)

