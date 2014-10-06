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
import pygmaps
import webbrowser
import os

def usage():
    print "%s Usage"%sys.argv[0]
    print "    -h: help"
    print "    -b <bssid>: BSSID to search. Format: xx:xx:xx:xx:xx:xx"
    print "    -d: Turn on debugging."
    print "    -w: Opens web browser with the generated map"
    print "    -o: Custom filename for output map"
    sys.exit()

# Defaults
bssid   = None
DEBUG  = False
output_file = "mymap.draw.html"
#writemap = TRUE
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

# Get BSSID from Apple and print results
applewloc.print_locs(applewloc.AppleWloc(bssid))
networks = applewloc.AppleWloc(bssid)
#print "networks:",networks


    # Create Google map of networks
mymap = pygmaps.maps((networks[bssid][0]),(networks[bssid][1]), 8)
for e in networks:
    mymap.addpoint((networks[bssid][0]),(networks[bssid][1]),color = "#FF0000",title = bssid)
mymap.draw('./'+output_file)
output_file = os.path.abspath(output_file)
print "File written to:", output_file

# Open in web browser
if openbrowser == True:
    webbrowser.open_new_tab("file://"+output_file)
    print "%s Done."%sys.argv[0]

