#!/usr/bin/python
############################################################################
#                                                                          #
#  Name: Geolocate BSSIDs using Google                                     #
#                                                                          #
#  Description: BSSIDlookup accepts one input to the command line          #
#               and utilizes the iSniff GPS/undocumented API call to       #
#               determine location of APs                                  #
#                                                                          #
#  Usage: ./BSSIDlookup.py -b <xx:xx:xx:xx:xx:xx>                          #
#                                                                          #
#  Requirements: Python                                                    #
#                python-requests                                           #
#                BeautifulSoup                                             #
#                bs4                                                       #
#                iSniffGPS wloc (included)                                 #
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
import sys
import applewloc

def usage():
    print "%s Usage"%sys.argv[0]
    print "    -h: help"
    print "    -b <bssid>: BSSID to search. Format: xx:xx:xx:xx:xx:xx"
    print "    -d: Turn on debugging."
    sys.exit()

# Defaults
bssid   = None
DEBUG  = False

# Process options
ops = ['-b','-d','-h']

while len(sys.argv) > 1:
    op = sys.argv.pop(1)
    if op == '-b':
        # Get user input and make it all lower case
        bssid = sys.argv.pop(1).lower()
        if bssid.count(':') != 5: usage()
    if op == '-d':
        DEBUG = True
        applewloc.DEBUG = True
    if op == '-h':
        usage()
    if op not in ops:
        print "Unknown option:",op
        usage()

# Test for user input
if not bssid: usage()
if DEBUG: print "In bssid:",bssid

# Get BSSID from Apple and print results
applewloc.print_locs(applewloc.AppleWloc(bssid))

