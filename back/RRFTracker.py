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
import time
import sys
import getopt
import os

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
            if arg not in ['RRF', 'TEC', 'FON']:
                print 'Unknown room name (choose between \'RRF\', \'TEC\' and \'FON\')'
                sys.exit()
            s.room = arg

    # Set url
    if s.room == 'RRF':
        url = 'http://rrf.f5nlg.ovh/api/svxlink/RRF'
    elif s.room == 'TEC':
        url = 'http://rrf.f5nlg.ovh/api/svxlink/technique'
    elif s.room == 'FON':
        url = 'http://fon.f1tzo.com:81'


    # Create directory and copy asset if necessary

    if not os.path.exists(s.log_path):
        os.makedirs(s.log_path)
    if not os.path.exists(s.log_path + '/assets'):
        os.popen('cp -a /opt/RRFTracker_Web/front/assets ' + s.log_path)

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
            for q in xrange(0, 24):         # Clean histogram
                s.qso_hour[q] = 0
                s.node_count_hour[q] = 0
            s.node.clear()                  # Clear node history
            s.porteuse.clear()              # Clear porteuse history

        # Request HTTP datas
        try:
            r = requests.get(url, verify=False, timeout=10)
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

            # Clean call
            tmp = page[search_start:search_stop]
            tmp = tmp.replace('(', '')
            tmp = tmp.replace(') ', ' ')
            tmp = tmp.replace('\u0026U', '&')   # Replace ampersand...

            s.call_current = tmp

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
            if (s.stat_save is False and s.duration > 2):
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
        tmp = tmp.split(',')

        s.node_count = len(tmp)
        s.node_count_hour[s.hour] = s.node_count - sum(s.node_count_hour[:s.hour])

        # Compute duration
        if s.transmit is True and s.tot_current > s.tot_start:
            s.duration = int(s.tot_current) - int(s.tot_start)
        if s.transmit is False:
            s.duration = 0

        # Save log
        l.log_write(s.log_path, s.day, s.room, s.qso_hour, s.node, s.porteuse, s.call, s.call_date, s.call_time, s.node_count, s.node_count_hour, s.day_duration, s.call_current, s.duration)

        time.sleep(1)

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
