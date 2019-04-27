#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

import settings as s
import lib as l

import requests
import datetime
import os
import time
import sys
import getopt

def main(argv):

    # Check and get arguments
    try:
        options, remainder = getopt.getopt(argv, '', ['help', 'log-path=', 'room='])
    except getopt.GetoptError:
        l.usage()
        sys.exit(2)
    for opt, arg in options:
        if opt == '--help':
            l.usage()
            sys.exit()
        elif opt in ('--log-path'):
            s.log_path = arg
        elif opt in ('--room'):
            if arg not in ['RRF', 'TEC', 'INT', 'BAV', 'LOC']:
                print 'Unknown room name (choose between \'RRF\', \'TEC\', \'INT\', \'BAV\' and \'LOC\')'
                sys.exit()
            s.room = arg

    # Create directory and copy asset if necessary

    if not os.path.exists(s.log_path):
        os.makedirs(s.log_path)
    if not os.path.exists(s.log_path + '/assets'):
        os.popen('cp -a /opt/RRFTracker_Web/front/assets ' + s.log_path)

    # Create geolocalisation list

    data = [line.strip() for line in open('../data/wgs84.dat')]

    for line in data:
        tmp = line.split(' ')
        s.geolocalisation[tmp[0]] = tmp[1] + ' ' + tmp[2]

    # Boucle principale
    while(True):

        # If midnight...
        tmp = datetime.datetime.now()
        s.day = tmp.strftime('%Y-%m-%d')
        s.now = tmp.strftime('%H:%M:%S')
        s.hour = int(tmp.strftime('%H'))
        s.minute = int(s.now[3:-3])
        s.seconde = int(s.now[-2:])

        if(s.now[:5] == '00:00'):
            s.qso = 0
            s.day_duration = 0
            for q in xrange(0, 24):     # Clean histogram
                s.qso_hour[q] = 0
            s.node.clear()              # Clear node history
            s.porteuse.clear()          # Clear porteuse history

        # Request HTTP datas
        try:
            r = requests.get(s.url[s.room], verify=False, timeout=10)
            page = r.content
        except requests.exceptions.ConnectionError as errc:
            print ('Error Connecting:', errc)
        except requests.exceptions.Timeout as errt:
            print ('Timeout Error:', errt)

        search_start = page.find('TXmit":"')            # Search this pattern
        search_start += 8                               # Shift...
        search_stop = page.find('"', search_start)      # And close it...

        # If transmitter...
        if search_stop != search_start:

            if s.transmit is False:
                s.transmit = True

            s.call_current = page[search_start:search_stop]

            if (s.call_previous != s.call_current):
                s.tot_start = time.time()
                s.tot_current = s.tot_start
                s.call_previous = s.call_current

                for i in xrange(9, 0, -1):
                    s.call[i] = s.call[i - 1]
                    s.call_date[i] = s.call_date[i - 1]
                    s.call_time[i] = s.call_time[i - 1]

                s.call[0] = s.call_current

            else:
                if s.tot_start is '':
                    s.tot_start = time.time()
                    s.tot_current = s.tot_start

                    for i in xrange(9, 0, -1):
                        s.call[i] = s.call[i - 1]
                        s.call_date[i] = s.call_date[i - 1]
                        s.call_time[i] = s.call_time[i - 1]

                    s.call[0] = s.call_current
                else:
                    s.tot_current = time.time()

            s.duration = int(s.tot_current) - int(s.tot_start)

            # Save stat only if real transmit
            if (s.stat_save is False and s.duration > s.intempestif):
                s.node = l.save_stat_node(s.node, s.call[0], 0)
                s.qso += 1
                s.stat_save = True

            # Format call time
            tmp = datetime.datetime.now()
            s.now = tmp.strftime('%H:%M:%S')
            s.hour = int(tmp.strftime('%H'))

            s.qso_hour[s.hour] = s.qso - sum(s.qso_hour[:s.hour])

            s.call_date[0] = s.now
            s.call_time[0] = s.duration

        # If no Transmitter...
        else:
            if s.transmit is True:
                if s.stat_save is True:
                    if s.duration > 600:    # I need to fix this bug...
                        s.duration = 0
                    s.node = l.save_stat_node(s.node, s.call[0], s.duration)
                    s.day_duration += s.duration
                if s.stat_save is False:
                    tmp = datetime.datetime.now()
                    s.porteuse = l.save_stat_porteuse(s.porteuse, s.call[0], tmp.strftime('%H:%M:%S'))

                s.transmit = False
                s.stat_save = False
                s.tot_current = ''
                s.tot_start = ''

        # Count node
        search_start = page.find('nodes":[')                    # Search this pattern
        search_start += 9                                       # Shift...
        search_stop = page.find('],"TXmit"', search_start)      # And close it...

        tmp = page[search_start:search_stop]
        tmp = tmp.replace('"', '')
        s.node_list = tmp.split(',')

        for n in ['RRF', 'RRF2', 'RRF3', 'TECHNIQUE']:
            if n in s.node_list:
                s.node_list.remove(n)

        if s.node_list_old == []:
            s.node_list_old = s.node_list
        else:
            if s.node_list_old != s.node_list:
                if (list(set(s.node_list_old) - set(s.node_list))):
                    s.node_list_out = list(set(s.node_list_old) - set(s.node_list))
                    for n in s.node_list_out:
                        if n in s.node_list_in:
                            s.node_list_in.remove(n)
                    s.node_list_out = sorted(s.node_list_out)

                if (list(set(s.node_list) - set(s.node_list_old))):
                    s.node_list_in = list(set(s.node_list) - set(s.node_list_old))
                    for n in s.node_list_in:
                        if n in s.node_list_out:
                            s.node_list_out.remove(n)
                    s.node_list_in = sorted(s.node_list_in)

                s.node_list_old = s.node_list

        s.node_count = len(s.node_list)

        if s.node_count > s.node_count_max:
            s.node_count_max = s.node_count

        if s.node_count < s.node_count_min:
            s.node_count_min = s.node_count

        # Compute duration
        if s.transmit is True and s.tot_current > s.tot_start:
            s.duration = int(s.tot_current) - int(s.tot_start)
        if s.transmit is False:
            s.duration = 0

        # Save log
        l.log_write()

        time.sleep(1)

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
