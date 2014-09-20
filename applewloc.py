#!/usr/bin/python
############################################################################
#                                                                          #
#  Name: applewloc.py                                                      #
#                                                                          #
#  Description: Functions and process that provides access to the          #
#               wloc.py and wigle.py functionity                           #
#                                                                          #
#  Usage:       Import this file to access functionality                   #
#                                                                          #
#  Requirements: Python                                                    #
#                python-requests - for wloc.py and wigle.py                #
#                BeautifulSoup   - for wigle.py                            #
#                bs4             - for wigle.py                            #
#                iSniffGPS wloc (included) - for wloc.py                   #
#                protobuf        - for GSM_pb2.py                          #
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
import wloc
#from wigle import getLocation
import wigle

# Global variables
STATUS = False
DEBUG  = False

# Print the networks provided in a python dictionary 
def print_locs(networks):
    # Print networks and their location
    for key,value in networks.items():
        print key,":", value

# Use wloc to find a bssid
def AppleWloc(bssid=None):
    # If you give us nothing we return nothing
    if not bssid: return {}
    if DEBUG: print "applewloc bssid:",bssid.lower()

    # Query Apple for the bssid
    apdict = wloc.QueryBSSID(bssid.lower())
    # Print status if we are running large sets
    if STATUS: print ".",
    if STATUS: sys.stdout.flush()
    # Review returned values for the bssid
    networks = {key: value for key, value in apdict.items() if (key == bssid.lower()) and not (value[0] == -180.0)}
    # Return the values for the bssid
    if DEBUG: print "applewloc.network:",networks
    return networks

# Retrieve the Lat/Long of a single BSSID
def getBSSIDloc(bssid=None):
    # If you give us nothing we return nothing
    if not bssid: return [None,None] 
    bssid = bssid.lower()
    if DEBUG: print "applewloc bssid:",bssid

    # This should return a single network
    network = AppleWloc(bssid=bssid.lower())
    if DEBUG: print "getBSSIDloc.network:",network

    # Return the value of the dictionary
    if bssid in network: return network[bssid]
    return [None,None]

# Retrieve SSID using wigle
def getSSIDloc(ssid=None,cookie=None):
    # If you give us nothing we return nothing
    if not ssid or not cookie: return {}
    if DEBUG: print "getSSID.ssid:",ssid
    if DEBUG: print "getSSID.cookie:",cookie

    # Request ssid and return the dictionary that wigle returns
    # Wigle dictionary format: {'stayoffmylawn [00:25:9C:ED:0F:EB] [6]': (33.65253067, -112.03952026)}
    return wigle.getLocation(SSID=ssid,cauth=cookie)
