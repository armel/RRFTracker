#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

import os
import glob
import datetime
import time
import sys
import getopt
import json


# Ansi color
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Usage
def usage():
    print 'Usage: RRFTracker.py [options ...]'
    print
    print '--help               this help'
    print
    print 'Search settings:'
    print '  --path         set path to RRF files (default=/var/www/RRFTracker/)'
    print '  --pattern      set search pattern (default=current month)'
    print
    print '88 & 73 from F4HWN Armel'

def main(argv):

    room_list = {
        'RRF',
    }

    porteuse = dict()

    tmp = datetime.datetime.now()

    search_path = '/var/www/RRFTracker/'
    search_pattern = tmp.strftime('%Y-%m')

    # Check and get arguments
    try:
        options, remainder = getopt.getopt(argv, '', ['help', 'path=', 'pattern='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in options:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt in ('--path'):
            search_path = arg
        elif opt in ('--pattern'):
            search_pattern = arg

    print color.BLUE + 'Path ' + color.END + search_path,
    print ' with ',
    print color.BLUE + 'Pattern ' + color.END + search_pattern,
    print '...'

    time_super_total = 0

    for r in room_list:
        path = search_path + r + '-' + search_pattern + '-*/rrf.json'
        file = glob.glob(path)
        file.sort()

        time_total = 0

        for f in file:
            if os.path.isfile(f):
                rrf_json = open (f)
                rrf_data = json.load(rrf_json)

                for data in rrf_data['porteuseExtended']:
                    try:
                        porteuse[data[u'Indicatif'].encode('utf-8')] += data[u'TX']
                    except:
                        porteuse[data[u'Indicatif'].encode('utf-8')] = data[u'TX']

    tmp = sorted(porteuse.items(), key=lambda x: x[1])
    tmp.reverse()

    for e in tmp:
        print e

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
