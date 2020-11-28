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
import urllib3

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
            if arg not in ['RRF', 'RRF_V1', 'TECHNIQUE', 'INTERNATIONAL', 'BAVARDAGE', 'LOCAL', 'EXPERIMENTAL', 'FON']:
                print('Unknown room name (choose between \'RRF\', \'TECHNIQUE\', \'INTERNATIONAL\', \'BAVARDAGE\', \'LOCAL\', \'EXPERIMENTAL\' and \'FON\')')
                sys.exit()
            s.room = arg

    # Create directory and copy asset if necessary

    if not os.path.exists(s.log_path):
        os.makedirs(s.log_path)
    if not os.path.exists(s.log_path + '/' + 'assets'):
        os.popen('cp -a ../front/assets ' + s.log_path)

    tmp = datetime.datetime.now()
    s.day = tmp.strftime('%Y-%m-%d')

    s.log_path_day = s.log_path + '/' + s.room + '-' + s.day

    if not os.path.exists(s.log_path_day):
        os.makedirs(s.log_path_day)
        os.popen('cp /opt/RRFTracker/front/index.html ' + s.log_path_day + '/index.html')
        os.popen('ln -sfn ' + s.log_path_day + ' ' + s.log_path + '/' + s.room + '-today')

    # If restart on day...

    filename = s.log_path + '/' + s.room + '-today/rrf.json'
    if os.path.isfile(filename):
        l.restart()

    # Get user online
    l.log_user()

    # Load whereis dict
    l.whereis_load()
    
    # Load whois dict
    l.whois_load()

    # Boucle principale
    while(True):
        chrono_start = time.time()

        # If midnight...
        tmp = datetime.datetime.now()
        s.day = tmp.strftime('%Y-%m-%d')
        s.now = tmp.strftime('%H:%M:%S')
        s.hour = int(tmp.strftime('%H'))
        s.minute = int(s.now[3:-3])
        s.seconde = int(s.now[-2:])

        if(s.minute % 5 == 0 and s.seconde == 0):
            l.log_user()
            l.whereis_load()

        if(s.now[:5] == '00:00'):
            l.whois_load()

            s.log_path_day = s.log_path + '/' + s.room + '-' + s.day

            if not os.path.exists(s.log_path_day):
                os.makedirs(s.log_path_day)
                os.popen('cp /opt/RRFTracker/front/index.html ' + s.log_path_day + '/index.html')
                os.popen('ln -sfn ' + s.log_path_day + ' ' + s.log_path + '/' + s.room + '-today')

            s.qso = 0
            s.day_duration = 0
            for q in range(0, 24):      # Clean histogram
                s.qso_hour[q] = 0
            s.all.clear()               # Clear all history
            s.porteuse.clear()          # Clear porteuse history
            s.tot.clear()               # Clear tot history
            s.init = True               # Reset init

        # Request HTTP datas

        try:
            r = http.request('GET', s.room_list[s.room]['url'], timeout=0.5, retries=10)
            data = json.loads(r.data.decode('utf-8'))
            transmitter = data['transmitter']
        except:
            data = ''
            print('Failed', s.day, s.now)

        if data != '':

            # If transmitter...
            if transmitter != '':

                if s.transmit is False:
                    s.transmit = True

                s.call_current = l.sanitize_call(transmitter)

                if (s.call_previous != s.call_current):
                    s.tot_start = time.time()
                    s.tot_current = s.tot_start
                    s.call_previous = s.call_current

                    if s.call_date[0] == '' or s.call_date[0] > s.now:
                        blanc = 0
                    else:
                        blanc = l.convert_time_to_second(s.now) - l.convert_time_to_second(s.call_date[0])

                    for i in range(9, 0, -1):
                        s.call[i] = s.call[i - 1]
                        s.call_date[i] = s.call_date[i - 1]
                        s.call_blanc[i] = s.call_blanc[i - 1]
                        s.call_time[i] = s.call_time[i - 1]

                    s.call[0] = s.call_current
                    s.call_blanc[0] = l.convert_second_to_time(blanc)

                else:
                    if s.tot_start == '':
                        s.tot_start = time.time()
                        s.tot_current = s.tot_start

                        if s.call_date[0] == '' or s.call_date[0] > s.now:
                            blanc = 0
                        else:
                            blanc = l.convert_time_to_second(s.now) - l.convert_time_to_second(s.call_date[0])

                        for i in range(9, 0, -1):
                            s.call[i] = s.call[i - 1]
                            s.call_date[i] = s.call_date[i - 1]
                            s.call_blanc[i] = s.call_blanc[i - 1]
                            s.call_time[i] = s.call_time[i - 1]

                        s.call[0] = s.call_current
                        s.call_blanc[0] = l.convert_second_to_time(blanc)

                    else:
                        s.tot_current = time.time()

                s.duration = int(s.tot_current) - int(s.tot_start)

                # Save stat only if real transmit
                if (s.stat_save is False and s.duration > s.intempestif):
                    #s.node = l.save_stat_node(s.node, s.call[0], 0)
                    s.qso += 1
                    tmp = datetime.datetime.now() - datetime.timedelta(seconds=3)
                    s.qso_hour[s.hour] = s.qso - sum(s.qso_hour[:s.hour])
                    s.all = l.save_stat_all(s.all, s.call[0], tmp.strftime('%H:%M:%S'), l.convert_second_to_time(s.duration), True)
                    
                    s.stat_save = True

                # Format call time
                tmp = datetime.datetime.now()
                s.now = tmp.strftime('%H:%M:%S')
                s.hour = int(tmp.strftime('%H'))

                s.qso_hour[s.hour] = s.qso - sum(s.qso_hour[:s.hour])

                s.call_date[0] = s.now
                s.call_time[0] = s.duration

                if s.duration > s.intempestif:
                    s.all = l.save_stat_all(s.all, s.call[0], tmp.strftime('%H:%M:%S'), l.convert_second_to_time(s.duration), False)

            # If no Transmitter...
            else:
                if s.transmit is True:
                    if s.room == 'RRF':
                        if l.convert_second_to_time(s.duration) > s.tot_limit:
                            tmp = datetime.datetime.now()
                            s.tot = l.save_stat_tot(s.tot, s.call[0], tmp.strftime('%H:%M:%S'))

                    if s.stat_save is True:
                        if s.duration > 600:    # I need to fix this bug...
                            s.duration = 0
                        s.day_duration += s.duration
                    if s.stat_save is False:
                        tmp = datetime.datetime.now()
                        s.porteuse = l.save_stat_porteuse(s.porteuse, s.call[0], tmp.strftime('%H:%M:%S'))

                    s.transmit = False
                    s.stat_save = False
                    s.tot_current = ''
                    s.tot_start = ''

            # Node analyze

            s.node_list=[]
            for d in data['nodes']:
                if d not in ['RRF', 'RRF2', 'RRF3', 'TECHNIQUE', 'BAVARDAGE', 'INTERNATIONAL', 'LOCAL', 'EXPERIMENTAL']:
                    s.node_list.append(l.sanitize_call(d))    

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

        # Manage tempo if necessary

        chrono_stop = time.time()
        chrono_time = chrono_stop - chrono_start
        if chrono_time < s.main_loop:
            sleep = s.main_loop - chrono_time
        else:
            sleep = 0
        #print "Temps d'execution : %.2f %.2f secondes" % (chrono_time, sleep)
        sys.stdout.flush()
        time.sleep(sleep)

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
