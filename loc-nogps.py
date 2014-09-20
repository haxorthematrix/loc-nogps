#!/usr/bin/python
############################################################################
#                                                                          #
#  Name: Geolocate Kismet findings from .netxml and populate custom        #
#        Google map.                                                       #
#                                                                          #
#  Description: kislocate accepts one or more Kismet .netxml files,        #
#               and utilizes the iSniff GPS/undocumented API call to       #
#               determine location of APs based on BSSID, without the need #
#               for a GPS at time of capture.                              #
#                                                                          #
#  Usage: ./loc-nogps.py -h                                                #
#         ./loc-nogps.py /path/to/kismet-netxml/  output-map-filename      #
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
#  Date: September 17, 2014                                                #
#                                                                          #
############################################################################

import os    
import sys
import xml.etree.ElementTree as ET
from string import lower
import wloc
import pygmaps
import webbrowser
import applewloc

def processnetworks(xml_dir):
    # cycle through each file in the directory
    files_in_dir = os.listdir(xml_dir)
    for file_in_dir in files_in_dir:
        if file_in_dir[-7:] == ".netxml":
            print "Adding file: ", file_in_dir 
            log_file_list.append(file_in_dir)

            xml_tree = ET.parse(xml_dir + file_in_dir)
            xml_root = xml_tree.getroot()
            network_essid = []
            network_bssid = []       
            networks = [] 
            
            # loop through each XML node of type "wireless-network"
            for network in xml_root.findall('wireless-network'):
                network_type = network.get('type')
                if network_type == 'probe': continue
                # set default values
                networks.append({'type':'n/a','bssid':'n/a','essid':'n/a','lat':'0','long':'0'})
                networks[-1]['type'] = network_type
              
                for network_detail in network:
                    if network_detail.tag == 'SSID':
                        for child_network in network_detail:
                            if child_network.tag == 'essid':
                                networks[-1]['essid'] = child_network.text
                    if network_detail.tag == 'BSSID':
                        networks[-1]['bssid'] = network_detail.text
                        #retrieve latlong
                        new_lat,new_long = applewloc.getBSSIDloc(network_detail.text)
                        if (new_lat == -180 or not new_lat) or (new_long == -180 or not new_long):
                            networks.pop(-1)
                            continue # skips rest of the for loop and goes to next iteration
                        networks[-1]['lat'] = new_lat
                        networks[-1]['long'] = new_long
    return networks

def print_nets(networks):
    print "Printing Networks:"
    for e in networks:
        print "   ",e

if __name__ == "__main__":

    def usage():
        print "%s Usage"%sys.argv[0]
        print "    -h: help"
        print "    -f <logfilepath>: A directory containing one or more Kismet .netxml log files. kislocate will process all .netxml files in the directory but will ignore all other files. Geolocate Kism findings from .netxml and populate custom Google map."
        print "    -o <output file name>: The name of the output file to write results. This will be written to the current working directory. Default: mymap.draw.html"
        print "    -w: Open results in web browser. Default: off"
        print "    -d <level>: Turn on debugging. Level 0 prints networks to be displayed. Level 1 prints networks as they are searched via wloc."
        sys.exit()

    # Defaults
    DEBUG  = False
    applewloc.DEBUG = False
    openweb = False
    network_matrix = []
    bssid_list = []
    log_file_list = []
    output_file = 'mymap.draw.html'

    # Process options
    ops = ['-f','-w','-o','-d','-h']

    while len(sys.argv) > 1:
        op = sys.argv.pop(1)
        if op == '-f':
            log_file_path = sys.argv.pop(1)
        if op == '-o':
            output_file = sys.argv.pop(1)
        if op == '-d':
            op = int(sys.argv.pop(1))
            if op > 0: DEBUG = True
            if op > 1: applewloc.DEBUG = True
        if op == '-w':
            openweb = True
        if op == '-h':
            usage()
        if op not in ops:
            print "Unknown option:",op
            usage()

    # add the ending slash in case it was left off
    if log_file_path[-1:] <> "/":
        log_file_path = log_file_path + "/"

    # Process xml files and retrieve network information
    networks = processnetworks(log_file_path)
    if DEBUG: print_nets(networks)

    # Create Google map of networks
    mymap = pygmaps.maps(networks[0]['lat'],networks[0]['long'], 8)
    for e in networks:
        mymap.addpoint(e['lat'],e['long'],color = "#FF0000",title = e['essid'])
    mymap.draw('./'+output_file)
    output_file = os.path.abspath(output_file)
    print "File written to:", output_file

    # Open in web browser
    if openweb: webbrowser.open_new_tab("file://"+output_file)
    print "%s Done."%sys.argv[0]
