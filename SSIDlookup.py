#!/usr/bin/python
############################################################################
#                                                                          #
#  Name: Geolocate SSIDs using Google and WiGLE                            #
#                                                                          #
#  Description: SSIDlookup accepts one input to the command line           #
#               and utilizes WiGLE to obtain the BSSID which uses the      #
#               iSniff GPS/undocumented API call to determine location of  #
#               APs.                                                       #
#                                                                          #
#  Usage: ./SSIDlookup.py <SSID> <cookie>                                  #
#                                                                          #
#  Requirements: Python                                                    #
#                python-requests                                           #
#                BeautifulSoup                                             #
#                bs4                                                       #
#                iSniffGPS wloc (included)                                 #
#                A cookie from WiGLE input into wigle.py                   #
#                  (obtain from a browser after logging in here:           #
#                  http://WiGLE.net/gps/gps/GPSDB/login)                   # 
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
    print "    -s <ssid>: SSID to search. Put SSIDs with spaces and special characters in double quotes."
    print "    -c <cookie>: The Wigle cookie to use. This requires a Wigle account with an active session or unexpired cookie."
    print "    -d: Turn on debugging."
    sys.exit()

# Defaults
ssid   = None
cookie = None       # Update this value with your 10 year Wigle cookie
DEBUG  = False

# Process options
ops = ['-s','-c','-d','-h']

while len(sys.argv) > 1:
    op = sys.argv.pop(1)
    if op == '-s':
        ssid = sys.argv.pop(1)
    if op == '-c':
        cookie = sys.argv.pop(1)
    if op == '-d':
        DEBUG = True
        applewloc.DEBUG = True
    if op == '-h':
        usage()
    if op not in ops:
        print "Unknown option:",op
        usage()

# Test for user input
if not ssid or not cookie: usage()
if DEBUG: print "In ssid:",ssid
if DEBUG: print "In cookie:",cookie

# Get list of possible BSSIDs by searching Wigle for specific SSID
bssids = applewloc.getSSIDloc(ssid=ssid,cookie=cookie)

# Process each of the BSSIDs returned by Wigle
# Wigle dictionary format: {'stayoffmylawn [00:25:9C:ED:0F:EB] [6]': (33.65253067, -112.03952026)
for key,value in bssids.items():
    if key:
        key = key.split()[1][1:-1]
    else:
        continue
    #print_locs(AppleWloc(bssid=key))
    networks = applewloc.AppleWloc(bssid=key)
    applewloc.print_locs(networks)
