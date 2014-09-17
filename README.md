loc-nogps
=========
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
