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
#                Kismet .netxml log files                                  #
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
import datetime
import xml.etree.ElementTree as ET
import argparse
from string import lower
import wloc
import pygmaps
import webbrowser


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
                        new_lat,new_long = AppleWloc(str(network_detail.text),str(child_network.text))
                        if (new_lat == -180) or (new_long == -180):
                            networks.pop(-1)
                            continue # skips rest of the for loop and goes to next iteration
                        networks[-1]['lat'] = new_lat
                        networks[-1]['long'] = new_long
    for e in networks:
        print e
    return networks

def AppleWloc(bssid,essid):
    template='apple-wloc.html'
    bssid=lower(bssid)
    apdict = wloc.QueryBSSID(bssid)
    for key,value in apdict.items():
        if key == lower(str(bssid)):
            print key,"::", value
            break
    return value

if __name__ == "__main__":

    # variables
    network_matrix = []
    bssid_list = []
    log_file_list = []

#now = datetime.datetime.now()
    # used on the HTML page output
    #   timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # process command-line arguments
    parser = argparse.ArgumentParser(description='Kismet Geolocation Google Map Generator v.1.0 ')
    parser.add_argument('log_file_path', metavar='LogFilePath',
                        help='A directory containing one or more Kismet .netxml log files. kislocate will process all .netxml files in the directory but will ignore all other files. Geolocate Kism findings from .netxml and populate custom Google map')
    args = parser.parse_args()
    #output_format = args.o
    # add the ending slash in case it was left off
    if args.log_file_path[-1:] <> "/":
        args.log_file_path = args.log_file_path + "/"

    networks = processnetworks(args.log_file_path)
    mymap = pygmaps.maps(networks[0]['lat'],networks[0]['long'], 8)
    for e in networks:
        mymap.addpoint(e['lat'],e['long'],color = "#FF0000",title = e['essid'])
    mymap.draw('./mymap.draw.html')
    file = os.path.abspath("mymap.draw.html")
    webbrowser.open_new_tab("file://"+file)