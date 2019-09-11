#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

import settings as s

import requests
import datetime
import os
import time
import locale
import re
import json

from random import randrange

# Usage
def usage():
    print 'Usage: RRFTracker.py [options ...]'
    print
    print '--help               this help'
    print
    print 'Room settings:'
    print '  --room ROOM        set room (default=RRF, choose between [RRF, RRF_V1, TECHNIQUE, INTERNATIONAL, BAVARDAGE, LOCAL])'
    print
    print 'Log settings:'
    print '  --log-path         set the location of log files'
    print
    print '88 & 73 from F4HWN Armel'

# Convert second to time
def convert_second_to_time(time):
    hours = time // 3600
    time = time - (hours * 3600)

    minutes = time // 60
    seconds = time - (minutes * 60)

    if hours == 0:
        return str('{:0>2d}'.format(int(minutes))) + ':' + str('{:0>2d}'.format(int(seconds)))
    else:
        return str('{:0>2d}'.format(int(hours))) + ':' + str('{:0>2d}'.format(int(minutes))) + ':' + str('{:0>2d}'.format(int(seconds)))

# Convert time to second
def convert_time_to_second(time):
    if len(time) > 5:
        format = [3600, 60, 1]
    else:
        format = [60, 1]        
    
    return sum([a * b for a, b in zip(format, map(int, time.split(':')))])

# Save stats
def save_stat_node(history, call, duration=0):
    if call != '':
        try:
            if duration == 0:
                history[call][0] += 1
            else:
                history[call][1] += duration
        except KeyError:
            history[call] = [1, duration]

    return history

# Save stats
def save_stat_porteuse(history, call, duration=0):
    if call != '':
        try:
            history[call][0] += 1
            history[call].append(duration)
        except KeyError:
            history[call] = [1, duration]

    return history

# Save stats
def save_stat_tot(history, call, duration=0):
    if call != '':
        try:
            history[call][0] += 1
            history[call].append(duration)
        except KeyError:
            history[call] = [1, duration]

    return history

# Save stats
def save_stat_all(history, call, hour='00:00', duration=0):
    if call != '':
        try:
            history[call][0] += 1
            a = convert_time_to_second(history[call][1])
            b = convert_time_to_second(duration)
            history[call][1] = convert_second_to_time(a + b)
            history[call].append(hour)
            history[call].append(duration)
        except KeyError:
            history[call] = [1, duration, hour, duration]

    return history

# Log write for history
def log_write():
    data = ''
    data += '{\n'

    # Refresh always
    data += log_abstract()
    data += log_activity()
    data += log_news()
    data += log_transmit()
    data += log_last()
    data += log_best()
    data += log_all()
    data += log_node()
    data += log_porteuse()
    data += log_tot()

    if s.init is False:
        data += log_elsewhere()

    data += '}\n'

    file = open(s.log_path_day + '/' + 'rrf_new.json', 'w')
    file.write(data)
    file.close()

    os.rename(s.log_path_day + '/' + 'rrf_new.json', s.log_path_day + '/' + 'rrf.json')

    if s.init is True:
        time.sleep(1)
        s.init = False

    return 0

# Log abstract
def log_abstract():

    data = '"abstract":\n'
    data += '[\n'

    locale.setlocale(locale.LC_TIME, '')

    tmp = datetime.datetime.now()
    now = tmp.strftime(' du %A %d/%m/%Y à %H:%M')

    data += '{\n'
    data += '\t"Salon": "' + s.room + '",\n'
    data += '\t"Date": "' + now.lower() + '",\n'
    data += '\t"TX total": ' + str(sum(s.qso_hour)) + ',\n'
    data += '\t"Emission cumulée": "' + convert_second_to_time(s.day_duration + s.duration) + '",\n'
    data += '\t"Nœuds actifs": ' + str(len(s.node)) + ',\n'
    data += '\t"Nœuds connectés": ' + str(s.node_count) + ',\n'
    data += '\t"Indicatif": "' + s.call_current + '",\n'
    data += '\t"TOT": ' + str(s.duration) + ',\n'
    data += '\t"User": ' + str(s.user_count) + ',\n'

    tmp = ''
    for n in s.node_list_in:
        tmp += str(n) + ', '
    tmp = tmp[:-2]

    data += '\t"Nœuds entrants": "' + tmp + '",\n'

    tmp = ''
    for n in s.node_list_out:
        tmp += str(n) + ', '
    tmp = tmp[:-2]

    data += '\t"Nœuds sortants": "' + tmp + '",\n'
    data += '\t"Nœuds max": ' + str(s.node_count_max) + ',\n'
    data += '\t"Nœuds min": ' + str(s.node_count_min) + '\n'
    data += '},\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '],\n'

    return data

# Log transmit
def log_transmit():

    if s.duration == 0:
        s.call_current = ''

    if s.call_current == '':
        s.duration = 0

    latitude = 0
    longitude = 0

    if s.call_current != '':
        tmp = s.call_current.split(' ')
        if (len(tmp) > 1):
            if(tmp[1] in s.geolocalisation):
                tmp = s.geolocalisation[tmp[1]].split(' ')
                latitude = tmp[0]
                longitude = tmp[1]

    data = '"transmit":\n'
    data += '[\n'

    data += '{\n'
    data += '\t"Indicatif": "' + s.call_current + '",\n'
    data += '\t"Latitude": ' + str(latitude) + ',\n'
    data += '\t"Longitude": ' + str(longitude) + ',\n'
    data += '\t"TOT": ' + str(s.duration) + '\n'
    data += '},\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '],\n'

    return data

# Log history
def log_activity():

    data = '"activity":\n'
    data += '[\n'

    l = 1
    for i in xrange(0, 24):

        x = str('{:0>2d}'.format(int(i)))
        y = str('{:0>2d}'.format(int(l)))
        z = str(s.qso_hour[i])

        x += 'h - ' + y + 'h'

        l += 1

        if l == 24:
            l = 0

        data += '{\n'
        data += '\t"Hour": "' + x + '",\n'
        data += '\t"TX": ' + z + '\n'
        data += '},\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '],\n'

    return data

# Log last
def log_last():

    data = '"last":\n'
    data += '[\n'

    p = 0

    for i in xrange(0, 10):
        if s.call_date[i] == '':
            break
        data += '{\n'
        data += '\t"Heure": "' + s.call_date[i] + '",\n'
        data += '\t"Indicatif": "' + s.call[i] + '",\n'
        data += '\t"Durée": "' + convert_second_to_time(s.call_time[i]) + '"\n'
        data += '},\n'

        p += 1

    if p > 0:
        last = data.rfind(',')
        data = data[:last] + '' + data[last + 1:]

    data += '],\n'

    return data

# Log best
def log_best():
    tmp = sorted(s.node.items(), key=lambda x: x[1][0])
    tmp.reverse()

    limit = 20
    data = '"best":\n'

    data += '[\n'

    p = 1
    for c, t in tmp:
        data += '{\n'
        data += '\t"Indicatif": "' + c + '",\n'
        data += '\t"TX": ' + str(t[0]) + '\n'
        data += '},\n'

        p += 1
        if p > limit:
            break

    if p > 1:
        last = data.rfind(',')
        data = data[:last] + '' + data[last + 1:]

    data += '],\n'

    return data

# Log node list
def log_node():

    data = '"nodeExtended":\n'
    data += '[\n'

    width = 4

    tmp = []
    for n in s.node_list:
        tmp.append(n)
    node_list = sorted(tmp)

    total = len(node_list)
    line = (total / width)

    complete = total - (line * width)

    if complete != 0:
        line += 1
        complete = (line * width) - total
        for n in xrange(0, complete):
            node_list.append('')

    limit = len(node_list)
    indice = 0

    while(indice < limit):
        data += '{\n'
        for e in xrange(0, width - 1):
            data += '\t"Node '+ str(e) +'": "' + node_list[indice + e] + '",\n'
        data += '\t"Node '+ str(e + 1) +'": "' + node_list[indice + e + 1] + '"\n'
        data += '},\n'
        indice += width

    if limit != 0:
        last = data.rfind(',')
        data = data[:last] + '' + data[last + 1:]

    data += '],\n'

    return data

# Log porteuse
def log_porteuse():
    tmp = sorted(s.porteuse.items(), key=lambda x: x[1])
    tmp.reverse()

    data = '"porteuseExtended":\n'

    data += '[\n'

    p = 1
    for c, t in tmp:
        data += '{\n'
        data += '\t"Pos": "' + str('{:0>3d}'.format(int(p))) + '",\n'
        data += '\t"Indicatif": "' + c + '",\n'
        data += '\t"TX": ' + str(t[0]) + ',\n'

        tmp = ''
        for e in t[1:]:
            tmp += str(e) + ', '
        tmp = tmp[:-2]

        data += '\t"Date": "' + str(tmp) + '"\n'
        data += '},\n'

        p += 1

    if p > 1:
        last = data.rfind(',')
        data = data[:last] + '' + data[last + 1:]

    data += '],\n'

    return data

# Log tot
def log_tot():
    tmp = sorted(s.tot.items(), key=lambda x: x[1])
    tmp.reverse()

    data = '"totExtended":\n'

    data += '[\n'

    p = 1
    for c, t in tmp:
        data += '{\n'
        data += '\t"Pos": "' + str('{:0>3d}'.format(int(p))) + '",\n'
        data += '\t"Indicatif": "' + c + '",\n'
        data += '\t"TX": ' + str(t[0]) + ',\n'

        tmp = ''
        for e in t[1:]:
            tmp += str(e) + ', '
        tmp = tmp[:-2]

        data += '\t"Date": "' + str(tmp) + '"\n'
        data += '},\n'

        p += 1

    if p > 1:
        last = data.rfind(',')
        data = data[:last] + '' + data[last + 1:]

    data += '],\n'

    return data

# Log all
def log_all():
    tmp = sorted(s.all.items(), key=lambda x: x[1][1])
    tmp.reverse()

    data = '"allExtended":\n'

    data += '[\n'

    p = 1
    for c, t in tmp:
        data += '{\n'
        data += '\t"Pos": "' + str('{:0>3d}'.format(int(p))) + '",\n'
        data += '\t"Indicatif": "' + c + '",\n'
        data += '\t"TX": ' + str(t[0]) + ',\n'
        data += '\t"Durée": "' + str(t[1]) + '",\n'

        heure = ''
        chrono = ''
        
        limit = len(t[2:])
        limit += 1

        for e in xrange(2, limit, 2):
            heure += str(t[e]) + ', '
            chrono += str(t[e + 1]) + ', '

        heure = heure[:-2]
        chrono = chrono[:-2]

        data += '\t"Heure": "' + str(heure) + '",\n'
        data += '\t"Chrono": "' + str(chrono) + '"\n'

        data += '},\n'

        p += 1

    if p > 1:
        last = data.rfind(',')
        data = data[:last] + '' + data[last + 1:]

    data += '],\n'

    return data

# Log news
def log_news():
    message_node = ''
    message = ''

    # Nœuds entrants

    tmp = ''
    for n in s.node_list_in:
        tmp += str(n) + ', '
    tmp = tmp[:-2]

    if tmp != '':
        if len(s.node_list_in) == 1:
            message_node += 'Nœud entrant : ' + tmp + '. '
        else:
            message_node += 'Nœuds entrants : ' + tmp + '. '

    # Nœuds sortants

    tmp = ''
    for n in s.node_list_out:
        tmp += str(n) + ', '
    tmp = tmp[:-2]

    if tmp != '':
        if len(s.node_list_out) == 1:
            message_node += 'Nœud sortant : ' + tmp + '. '
        else:
            message_node += 'Nœuds sortants : ' + tmp + '. '

    if s.message_node_old != message_node:
        s.message_current = message_node
        s.message_node_old = message_node
        s.message_timer = 0
        s.message_timer_limit = 100

    else:
        if s.message_timer > s.message_timer_limit:
            s.message_timer = 0
            tmp = randrange(5)

            if tmp == 0:
                s.message_current = 'Si vous testez un système, si vous faites des réglages, basculez sur un salon non occupé. '
            elif tmp == 1:
                s.message_current = 'Si vous constatez un problème (panne, perturbation, etc.), envoyez un mail à admin@f5nlg.ovh afin que nous puissions intervenir. '
            elif tmp == 2:
                s.message_current = 'Ne monopolisez pas le réseau. Soyez polis et courtois. Respectez les autres utilisateurs. '
            elif tmp == 3:
                s.message_current = 'Le salon RRF doit être considéré comme une « fréquence d\'appel », pensez à faire QSY sur un des salons annexes. '
            elif tmp == 4:
                s.message_current = 'Merci de faire des blancs de l\'ordre de 5 secondes. '

            s.message_timer_limit = len(s.message_current)
    
    s.message_timer += 1

    # Format JSON

    data = '"news":\n'

    data += '[\n'

    data += '{\n'

    data += '\t"Message": "' + s.message_current + '"\n'
    data += '},\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '],\n'

    return data

# Log everywhere
def log_elsewhere():
    room_other = s.room_list.copy()
    room_other.pop(s.room, None)

    data = '"elsewhere":\n'

    data += '[\n'
    data += '{\n'
    data += '\t"Scanner RRF": "Code DTMF",\n'

    for room in room_other:
        data += '\t"' + room + '": "' + room_other[room]['dtmf'] + '",\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '}, \n'
    data += '{\n'

    tx = []
    time = []
    call = []
    actif = []
    connected = []

    for room in room_other:
        filename = s.log_path + '/' + room + '-today/rrf.json'

        if os.path.isfile(filename):
            with open(filename, 'r') as content_file:
                content = content_file.read()

                # Indicatif 

                search_start = content.find('Indicatif": "')        # Search this pattern
                search_start += 13                                  # Shift...
                search_stop = content.find('"', search_start)       # And close it...

                tmp = content[search_start:search_stop]

                if tmp == '':
                    call.append("Aucune émission")
                else:
                    call.append(tmp)

                # Emission cumulée

                search_start = content.find('Emission cumulée": "') # Search this pattern
                search_start += 21                                  # Shift...
                search_stop = content.find('"', search_start)       # And close it...

                tmp = content[search_start:search_stop]

                time.append(tmp)

                # Emission cumulée
                search_start = content.find('TX total": ')          # Search this pattern
                search_start += 11                                  # Shift...
                search_stop = content.find(',', search_start)       # And close it...

                tmp = content[search_start:search_stop]

                tx.append(tmp)

                # Noeuds actifs
                search_start = content.find('Nœuds actifs": ')      # Search this pattern
                search_start += 15                                  # Shift...
                search_stop = content.find(',', search_start)       # And close it...

                tmp = content[search_start:search_stop]

                actif.append(tmp)

                # Noeuds connectés
                search_start = content.find('Nœuds connectés": ')   # Search this pattern
                search_start += 19                                  # Shift...
                search_stop = content.find(',', search_start)       # And close it...

                tmp = content[search_start:search_stop]

                connected.append(tmp)

    data += '\t"Scanner RRF": "Emission en cours",\n'
    tmp = 0

    for room in room_other:
        data += '\t"' + room + '": "' + call[tmp] + '",\n'
        tmp += 1

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '}, \n'
    data += '{\n'

    data += '\t"Scanner RRF": "TX total",\n'
    tmp = 0
    for room in room_other:
        data += '\t"' + room + '": "' + tx[tmp] + '",\n'
        tmp += 1

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '}, \n'
    data += '{\n'

    data += '\t"Scanner RRF": "Emission cumulée",\n'
    tmp = 0
    for room in room_other:
        data += '\t"' + room + '": "' + time[tmp] + '",\n'
        tmp += 1

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '}, \n'
    data += '{\n'

    data += '\t"Scanner RRF": "Nœuds actifs",\n'
    tmp = 0
    for room in room_other:
        data += '\t"' + room + '": "' + actif[tmp] + '",\n'
        tmp += 1

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '}, \n'
    data += '{\n'

    data += '\t"Scanner RRF": "Nœuds connectés",\n'
    tmp = 0
    for room in room_other:
        data += '\t"' + room + '": "' + connected[tmp] + '",\n'
        tmp += 1

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '}\n'
    data += ']\n'

    return data

# Log user
def log_user():

    try:
        r = requests.get('http://rrf.f5nlg.ovh:8080/server-status', verify=False, timeout=10)
        page = r.content
    except requests.exceptions.ConnectionError as errc:
        print ('Error Connecting:', errc)
    except requests.exceptions.Timeout as errt:
        print ('Timeout Error:', errt)

    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', page)
    ip = list(set(ip))

    return str(len(ip) - 1)

# Restart
def restart():

    filename = s.log_path + '/' + s.room + '-today/rrf.json'
    if os.path.isfile(filename):
        rrf_json = open (filename)
        rrf_data = json.load(rrf_json)

    # Section activity and abstract

    i = 0
    for data in rrf_data['activity']:
        s.qso_hour[i] = data['TX']
        i += 1

    s.qso = sum(s.qso_hour)

    for data in rrf_data['abstract']:
        s.day_duration = convert_time_to_second(data[u'Emission cumulée'])

    # Section last

    i = 0
    for data in rrf_data['last']:
        s.call[i] = data[u'Indicatif'].encode('utf-8')
        s.call_date[i] = data[u'Heure'].encode('utf-8')
        s.call_time[i] = convert_time_to_second(data[u'Durée'])
        i += 1

    # Section porteuse

    for data in rrf_data['porteuseExtended']:
        s.porteuse[data[u'Indicatif'].encode('utf-8')] = [data[u'TX'], data[u'Date'].encode('utf-8')]

    # Section tot

    for data in rrf_data['totExtended']:
        s.tot[data[u'Indicatif'].encode('utf-8')] = [data[u'TX'], data[u'Date'].encode('utf-8')]

    # Section all

    for data in rrf_data['allExtended']:
        s.all[data[u'Indicatif'].encode('utf-8')] = [data[u'TX'], data[u'Durée']]

        chrono = data['Chrono'].split(', ')
        heure = data['Heure'].split(', ')

        limit = len(chrono)

        for e in xrange(limit):
            s.all[data[u'Indicatif'].encode('utf-8')].append(heure[e])
            s.all[data[u'Indicatif'].encode('utf-8')].append(chrono[e])

    s.transmit = False

    return 0
