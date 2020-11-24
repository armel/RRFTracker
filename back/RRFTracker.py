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
            if arg not in ['RRF', 'TECHNIQUE', 'INTERNATIONAL', 'BAVARDAGE', 'LOCAL', 'EXPERIMENTAL', 'FON']:
                print('Unknown room name (choose between \'RRF\', \'TECHNIQUE\', \'INTERNATIONAL\', \'BAVARDAGE\', \'LOCAL\', \'EXPERIMENTAL\' and \'FON\')')
                sys.exit()
            s.room = arg

    # Create directory and copy asset if necessary
    for r in s.room_list:
        s.room = r
        if not os.path.exists(s.log_path):
            os.makedirs(s.log_path)
        if not os.path.exists(s.log_path + '/' + 'assets'):
            os.popen('cp -a ../front/assets ' + s.log_path)

        tmp = datetime.datetime.now()
        s.day = tmp.strftime('%Y-%m-%d')

        s.log_path_day[s.room] = s.log_path + '/' + s.room + '-' + s.day

        if not os.path.exists(s.log_path_day[s.room]):
            os.makedirs(s.log_path_day[s.room])
            os.popen('cp /opt/RRFTracker/front/index.html ' + s.log_path_day[s.room] + '/index.html')
            os.popen('ln -sfn ' + s.log_path_day[s.room] + ' ' + s.log_path + '/' + s.room + '-today')

        # If restart on day...

        filename = s.log_path + '/' + s.room + '-today/rrf.json'
        if os.path.isfile(filename):
            l.restart()

    # Get user online
    s.user_count = l.log_user()

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

        data = ''

        # Request HTTP datas
        try:
            r = requests.get(s.api_url, verify=False, timeout=2)
        except requests.exceptions.ConnectionError as errc:
            print(s.day, s.now, 'Error Connecting:', errc)
        except requests.exceptions.Timeout as errt:
            print(s.day, s.now, 'Timeout Error:', errt)

        # Controle de la validité du flux json
        try:
            data = r.json()
        except:
            pass

        if data != '':

            # Surf in room list
            for r in s.room_list:

                s.room = r

                if(s.minute % 5 == 0):
                    s.user_count = l.log_user()

                if(s.minute % 30 == 0):
                    l.whois_load()

                if(s.now[:5] == '00:00'):
                    s.log_path_day[s.room] = s.log_path + '/' + s.room + '-' + s.day

                    if not os.path.exists(s.log_path_day[s.room]):
                        os.makedirs(s.log_path_day[s.room])
                        os.popen('cp /opt/RRFTracker/front/index.html ' + s.log_path_day[s.room] + '/index.html')
                        os.popen('ln -sfn ' + s.log_path_day[s.room] + ' ' + s.log_path + '/' + s.room + '-today')

                    s.qso[s.room] = 0
                    s.day_duration[s.room] = 0
                    for q in range(0, 24):      # Clean histogram
                        s.qso_hour[s.room][q] = 0
                    s.all[s.room] = []          # Clear all history
                    s.porteuse[s.room] = []     # Clear porteuse history
                    s.tot[s.room] = []          # Clear tot history
                    s.init[s.room] = True       # Reset init

                try:
                    # If transmitter...
                    print('ici 1')
                    if data['transmitters'][s.room_list[s.room]['realname']] != None:

                        if s.transmit[s.room] is False:
                            s.transmit[s.room] = True

                        s.call_current[s.room] = l.sanitize_call(data['transmitters'][s.room_list[s.room]['realname']][2])
                        s.whereis_call[s.room] = data['transmitters'][s.room_list[s.room]['realname']][0]

                        print(s.room, s.call_current[s.room], s.whereis_call[s.room])

                        if (s.call_previous[s.room] != s.call_current[s.room]):
                            s.tot_start[s.room] = time.time()
                            s.tot_current[s.room] = s.tot_start[s.room]
                            s.call_previous[s.room] = s.call_current[s.room]

                            if s.call_date[s.room][0] == '' or s.call_date[s.room][0] > s.now:
                                blanc = 0
                            else:
                                blanc = l.convert_time_to_second(s.now) - l.convert_time_to_second(s.call_date[s.room][0])

                            for i in range(9, 0, -1):
                                s.call[s.room][i] = s.call[s.room][i - 1]
                                s.call_date[s.room][i] = s.call_date[s.room][i - 1]
                                s.call_blanc[s.room][i] = s.call_blanc[s.room][i - 1]
                                s.call_time[s.room][i] = s.call_time[s.room][i - 1]

                            s.call[s.room][0] = s.call_current[s.room]
                            s.call_blanc[s.room][0] = l.convert_second_to_time(blanc)

                        else:
                            if s.tot_start[s.room] == '':
                                s.tot_start[s.room] = time.time()
                                s.tot_current[s.room] = s.tot_start[s.room]

                                if s.call_date[s.room][0] == '' or s.call_date[s.room][0] > s.now:
                                    blanc = 0
                                else:
                                    blanc = l.convert_time_to_second(s.now) - l.convert_time_to_second(s.call_date[s.room][0])

                                for i in range(9, 0, -1):
                                    s.call[s.room][i] = s.call[s.room][i - 1]
                                    s.call_date[s.room][i] = s.call_date[s.room][i - 1]
                                    s.call_blanc[s.room][i] = s.call_blanc[s.room][i - 1]
                                    s.call_time[s.room][i] = s.call_time[s.room][i - 1]

                                s.call[s.room][0] = s.call_current[s.room]
                                s.call_blanc[s.room][0] = l.convert_second_to_time(blanc)

                            else:
                                s.tot_current[s.room] = time.time()

                        s.duration[s.room] = int(s.tot_current[s.room]) - int(s.tot_start[s.room])

                        # Save stat only if real transmit
                        if (s.stat_save[s.room] is False and s.duration[s.room] > s.intempestif[s.room]):
                            s.qso[s.room] += 1
                            tmp = datetime.datetime.now() - datetime.timedelta(seconds=3)
                            s.qso_hour[s.room][s.hour] = s.qso[s.room] - sum(s.qso_hour[s.room][:s.hour])
                            s.all[s.room] = l.save_stat_all(s.all[s.room], s.call[s.room][0], tmp.strftime('%H:%M:%S'), l.convert_second_to_time(s.duration[s.room]), True)
                            
                            s.stat_save[s.room] = True

                        # Format call time
                        tmp = datetime.datetime.now()
                        s.now = tmp.strftime('%H:%M:%S')
                        s.hour = int(tmp.strftime('%H'))

                        s.qso_hour[s.room][s.hour] = s.qso[s.room] - sum(s.qso_hour[s.room][:s.hour])

                        s.call_date[s.room][0] = s.now
                        s.call_time[s.room][0] = s.duration[s.room]

                        if s.duration[s.room] > s.intempestif[s.room]:
                            s.all[s.room] = l.save_stat_all(s.all[s.room], s.call[s.room][0], tmp.strftime('%H:%M:%S'), l.convert_second_to_time(s.duration[s.room]), False)

                        #sys.stdout.flush()


                    # If no Transmitter...
                    else:
                        if s.transmit[s.room] is True:

                            if s.room == 'RRF':
                                #print l.convert_second_to_time(s.duration), s.tot_limit
                                #sys.stdout.flush()
                                if l.convert_second_to_time(s.duration[s.room]) > s.tot_limit[s.room]:
                                    tmp = datetime.datetime.now()
                                    s.tot[s.room] = l.save_stat_tot(s.tot[s.room], s.call[s.room][0], tmp.strftime('%H:%M:%S'))

                            if s.stat_save[s.room] is True:
                                if s.duration[s.room] > 600:    # I need to fix this bug...
                                    s.duration[s.room] = 0
                                #s.node = l.save_stat_node(s.node, s.call[0], s.duration)
                                s.day_duration[s.room] += s.duration[s.room]
                            if s.stat_save[s.room] is False:
                                tmp = datetime.datetime.now()
                                s.porteuse[s.room] = l.save_stat_porteuse(s.porteuse[s.room], s.call[s.room][0], tmp.strftime('%H:%M:%S'))

                            s.transmit[s.room] = False
                            s.stat_save[s.room] = False
                            s.tot_current[s.room] = ''
                            s.tot_start[s.room] = ''

                    # Count node
                    s.node_list[s.room] = []

                    for d in data['nodes']:
                        if d[1] == s.room_list[s.room]['realname']:
                             s.node_list[s.room].append(l.sanitize_call(d[2]))

                    if s.node_list_old[s.room] == []:
                        s.node_list_old[s.room] = s.node_list[s.room]
                    else:
                        if s.node_list_old[s.room] != s.node_list[s.room]:
                            if (list(set(s.node_list_old[s.room]) - set(s.node_list[s.room]))):
                                s.node_list_out[s.room] = list(set(s.node_list_old[s.room]) - set(s.node_list[s.room]))
                                for n in s.node_list_out[s.room]:
                                    if n in s.node_list_in[s.room]:
                                        s.node_list_in[s.room].remove(n)
                                s.node_list_out[s.room] = sorted(s.node_list_out[s.room])

                            if (list(set(s.node_list[s.room]) - set(s.node_list_old[s.room]))):
                                s.node_list_in[s.room] = list(set(s.node_list[s.room]) - set(s.node_list_old[s.room]))
                                for n in s.node_list_in[s.room]:
                                    if n in s.node_list_out[s.room]:
                                        s.node_list_out[s.room].remove(n)
                                s.node_list_in[s.room] = sorted(s.node_list_in[s.room])

                            s.node_list_old[s.room] = s.node_list[s.room]

                    s.node_count[s.room] = len(s.node_list[s.room])

                    if s.node_count[s.room] > s.node_count_max[s.room]:
                        s.node_count_max[s.room] = s.node_count[s.room]

                    if s.node_count[s.room] < s.node_count_min[s.room]:
                        s.node_count_min[s.room] = s.node_count[s.room]

                    # Compute duration
                    if s.transmit[s.room] is True and s.tot_current[s.room] > s.tot_start[s.room]:
                        s.duration[s.room] = int(s.tot_current[s.room]) - int(s.tot_start[s.room])
                    if s.transmit[s.room] is False:
                        s.duration[s.room] = 0

                    # Save log
                    # print(s.now, r)
                    l.log_write()
                except:
                    pass
        else:
            print(s.day, s.now, 'JSON inconsistant')
    
        chrono_stop = time.time()
        chrono_time = chrono_stop - chrono_start
        if chrono_time < s.main_loop:
            sleep = s.main_loop - chrono_time
        else:
            sleep = 0
        #print("Temps d'execution : %.2f %.2f secondes" % (chrono_time, sleep))
        #sys.stdout.flush()
        time.sleep(sleep)

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
