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
#  Usage: ./BSSIDbrute.py <01:23:x:67:x:ab>                                #
#         an "x" should represent the octets to bruteforce                 #
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
import pygmaps
import webbrowser
import os

def usage():
    print "%s Usage"%sys.argv[0]
    print "    -h: help"
    print "    -b <bssid>: BSSID to search. Format: 01:23:x:67:x:ab. Search locations should be a single 'x'."
    print "    -d: Turn on debugging."
    print "    -w: Opens web browser. Requires -m"
    print "    -m: Generate google map. Defaults to mymap.draw.html"
    print "    -o: Custom filename map output"
    sys.exit()

# Defaults
bssid   = None
STATUS = False
DEBUG  = False
output_file = "mymap.draw.html"
writemap = True
mymap = None
openbrowser = False
networks = {}

# Process options
ops = ['-b','-d','-h','-o','-w']

while len(sys.argv) > 1:
    op = sys.argv.pop(1)
    if op == '-b':
        # Get user input and make it all lower case
        bssid = sys.argv.pop(1).lower()
        if bssid.count(':') != 5: usage()
    if op == '-d':
        DEBUG = True
        applewloc.DEBUG = True
    if op == '-o':
        output_file = sys.argv.pop(1)
    if op == '-w':
        openbrowser = True
    if op == '-h':
        usage()
    if op not in ops:
        print "Unknown option:",op
        usage()

# Test for user input
if not bssid: usage()
if DEBUG: print "In bssid:",bssid

# Build possible values. These will be lower.

max_octet = 256

octets = [chr(x).encode('hex') for x in range(max_octet)]

# Generate possible networks
re_chr = 'x'
if not bssid.count(re_chr) or bssid.count(re_chr) > 3:
    print "Expected input 12:x:45:x:67:x with max of 3 x\'s"
    sys.exit()
# First run
tmp = [bssid.replace('x',x,1) for x in octets]
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
for e in tmp:

    # Process each bssid
    network = applewloc.AppleWloc(bssid=e)
    #print "networks:",network
    networks.update(network)
    # Print each network discovered
    applewloc.print_locs(network)

#networks = applewloc.AppleWloc(bssid)
#print "networks:",networks


#if writemap == True:
    # Create Google map of networks
base_bssid = networks.keys()[0]
mymap = pygmaps.maps((networks[base_bssid][0]),(networks[base_bssid][1]), 4)
for e in networks.keys():
    mymap.addpoint(networks[e][0],networks[e][1],color = "#FF0000",title = [e])
mymap.draw('./'+output_file)
output_file = os.path.abspath(output_file)
print "File written to:", output_file

# Open in web browser
if openbrowser == True:
    webbrowser.open_new_tab("file://"+output_file)
    print "%s Done."%sys.argv[0]

