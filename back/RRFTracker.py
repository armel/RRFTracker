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

def main(argv):

    # Check and get arguments
    try:
        options, remainder = getopt.getopt(argv, '', ['help', 'log', 'room='])
    except getopt.GetoptError:
        l.usage()
        sys.exit(2)
    for opt, arg in options:
        if opt == '--help':
            l.usage()
            sys.exit()
        elif opt in ('--log'):
            s.log = True
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

    # Boucle principale
    s.timestamp_start = time.time()

    while(True):

        # If midnight...
        tmp = datetime.datetime.now()
        s.day = tmp.strftime('%Y-%m-%d')
        s.now = tmp.strftime('%H:%M:%S')
        s.hour = int(tmp.strftime('%H'))
        s.minute = int(s.now[3:-3])
        s.seconde = int(s.now[-2:])

        if(s.now[:5] == '00:00'):
            s.qso_total += s.qso
            s.qso = 0
            for q in xrange(0, 24):         # Clean histogram
                s.qso_hour[q] = 0
            s.history.clear()               # Clear history

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

                for i in xrange(4, 0, -1):
                    s.call[i] = s.call[i - 1]
                    s.call_time[i] = s.call_time[i - 1]

                s.call[0] = s.call_current

                s.history = l.save_stat(s.history, s.call[1])
                s.qso += 1
            else:
                if s.tot_start is '':
                    s.tot_start = time.time()
                s.tot_current = time.time()
                if (s.blanc is True):         # Stat (same call but new PTT...)
                    s.history = l.save_stat(s.history, s.call[0])

            s.blanc = False

            # Format call time
            tmp = datetime.datetime.now()
            s.now = tmp.strftime('%H:%M:%S')
            s.hour = int(tmp.strftime('%H'))

            s.qso_hour[s.hour] = s.qso - sum(s.qso_hour[:s.hour])

            s.call_time[0] = s.now

        # If no Transmitter...
        else:
            if s.blanc is False:
                s.blanc = True
                duration = int(s.tot_current) - int(s.tot_start)
                s.tot_current = ''
                s.tot_start = ''
                if duration > 3:
                    s.qso += 1

            search_start = page.find('nodes":[')                    # Search this pattern
            search_start += 9                                       # Shift...
            search_stop = page.find('],"TXmit"', search_start)      # And close it...

            tmp = page[search_start:search_stop]
            tmp = tmp.split(',')

            s.node = len(tmp)

        # Write log

        if s.log is True:
            l.log_write(s.log_path, s.day, s.room, s.qso_hour, s.history, s.call, s.call_time, s.node)

        time.sleep(2)

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
