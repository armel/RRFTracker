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
    print('Usage: RRFTracker.py [options ...]')
    print()
    print('--help               this help')
    print()
    print('Room settings:')
    print('  --room ROOM        set room (default=RRF, choose between [RRF, TECHNIQUE, INTERNATIONAL, BAVARDAGE, LOCAL, EXPERIMENTAL, FON])')
    print()
    print('Log settings:')
    print('  --log-path         set the location of log files')
    print()
    print('88 & 73 from F4HWN Armel')

# Sanitize call
def sanitize_call(call):
    return call.translate(str.maketrans('', '', '\\\'!@#$"'))

# Whois load
def whois_load():
    with open(os.path.join(os.path.dirname(__file__), '../data/whois.dat')) as f:
        for line in f:
            tmp = line.split(';')
            s.whois_list[tmp[0]] = line
    return True

# Whois call
def whois_call(call):
    if call in s.whois_list:
        return s.whois_list[call]

    if s.room != 'FON':
        if os.path.isfile(os.path.join(os.path.dirname(__file__), '../data/inconnu.dat')):
            with open(os.path.join(os.path.dirname(__file__), '../data/inconnu.dat')) as f:
                for line in f:
                    if line.strip() == call.strip():
                        return False

        with open(os.path.join(os.path.dirname(__file__), '../data/inconnu.dat'), 'a') as f:
            f.write(call + '\n')

    return False

# Whereis load
def whereis_load():
    whereis_data = ''
    # Requete HTTP vers l'api de F1EVM
    try:
        r = requests.get(s.whereis_api, verify=False, timeout=0.50)
    except requests.exceptions.ConnectionError as errc:
        #print ('Error Connecting:', errc)
        pass
    except requests.exceptions.Timeout as errt:
        #print ('Timeout Error:', errt)
        pass

    # Controle de la validité du flux json
    try:
        whereis_data = r.json()
    except:
        pass

    if whereis_data != '':
        for item in whereis_data['nodes']:
            s.whereis_list[item[2]] = item[0]
    return True

# Whereis call
def whereis_call(call):
    if call in s.whereis_list:
        return s.whereis_list[call]
    return False

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
    
    return sum([a * b for a, b in zip(format, list(map(int, time.split(':'))))])

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
def save_stat_all(history, call, hour, duration, new=False):
    if call != '':
        try:
            if new is True:
                history[call][0] += 1
                history[call].append(hour)
                history[call].append(duration)
            else:
                history[call].pop()
                history[call].append(duration)

            limit = len(history[call])
            total = 0

            for e in range(3, limit, 2):
                #print limit, history[call], history[call][e]
                total += convert_time_to_second(history[call][e])

            history[call][1] = convert_second_to_time(total)


        except KeyError:
            history[call] = [1, '00:00', hour, '00:00']

    return history

# Log write for history
def log_write():
    data = ''
    data_tiny = ''

    data += '{\n'

    # Flux commun rrf.json et rrf_tiny.json
    data += log_abstract()
    data += log_activity()
    data += log_transmit()
    data += log_last()
    if s.init is False:
        data += log_elsewhere()

    data_tiny = data

    # Flux rrf.json
    data += log_all()
    data += log_best()
    data += log_node()
    data += log_porteuse()
    data += log_tot()
    data += log_type()
    data += log_iptable()
    data += log_news()
    data += '}\n'

    # Ecriture de flux rrf.json
    file = open(s.log_path_day + '/' + 'rrf_new.json', 'w')
    file.write(data)
    file.close()

    os.rename(s.log_path_day + '/' + 'rrf_new.json', s.log_path_day + '/' + 'rrf.json')

    # Flux rrf_tiny.json
    data_tiny += log_all_tiny()
    data_tiny += '}\n'

    # Ecriture du flux rrf_tiny_json
    file = open(s.log_path_day + '/' + 'rrf_tiny.json', 'w')
    file.write(data_tiny)
    file.close()

    # Si init, on fait une pose

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
    now = tmp.strftime(' du %d/%m/%Y à %H:%M')

    data += '{\n'
    data += '\t"Version": "' + s.version + '",\n'
    data += '\t"Salon": "' + s.room + '",\n'
    data += '\t"Date": "' + now.lower() + '",\n'
    data += '\t"TX total": ' + str(sum(s.qso_hour)) + ',\n'
    data += '\t"Emission cumulée": "' + convert_second_to_time(s.day_duration + s.duration) + '",\n'
    data += '\t"Links actifs": ' + str(len(s.all)) + ',\n'
    data += '\t"Links connectés": ' + str(s.node_count) + ',\n'
    data += '\t"Indicatif": "' + s.call_current + '",\n'
    data += '\t"TOT": ' + str(s.duration) + ',\n'
    data += '\t"User": ' + str(s.user_count) + ',\n'

    tmp = ''
    for n in s.node_list_in:
        tmp += str(n) + ', '
    tmp = tmp[:-2]

    data += '\t"Links entrants": "' + tmp + '",\n'

    tmp = ''
    for n in s.node_list_out:
        tmp += str(n) + ', '
    tmp = tmp[:-2]

    data += '\t"Links sortants": "' + tmp + '",\n'
    data += '\t"Links max": ' + str(s.node_count_max) + ',\n'
    data += '\t"Links min": ' + str(s.node_count_min) + ',\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '}\n'
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

    data = '"transmit":\n'
    data += '[\n'

    data += '{\n'
    data += '\t"Indicatif": "' + s.call_current + '",\n'
    if s.call_current != '':
        tmp = whois_call(s.call_current)
        if tmp is False:
            tmp = '-;-;Link Inconnu;-;-;0;0;-;-' # Indicatif;Type;Description;Tone;Locator;Longitude;Latitude;Sysop;Prenom

        tmp = tmp.split(';')

        data += '\t"Type": "' + tmp[1] + '",\n'
        data += '\t"Description": "' + tmp[2] + '",\n'
        data += '\t"Tone": "' + tmp[3] + '",\n'
        data += '\t"Locator": "' + tmp[4] + '",\n'
        data += '\t"Longitude": ' + str(tmp[5].strip()) + ',\n'
        data += '\t"Latitude": ' + str(tmp[6].strip()) + ',\n'
        data += '\t"Sysop": "' + tmp[7].strip() + '",\n'
        data += '\t"Prenom": "' + tmp[8].strip() + '",\n'

        tmp = whereis_call(s.call_current)
        if tmp is False:
            data += '\t"Serveur": "-",\n'
        else:
            data += '\t"Serveur": "' + str(tmp) + '",\n'

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
    for i in range(0, 24):

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

    for i in range(0, 10):
        if s.call_date[i] == '':
            break
        data += '{\n'
        data += '\t"Heure": "' + s.call_date[i] + '",\n'
        data += '\t"Indicatif": "' + s.call[i] + '",\n'
        data += '\t"Blanc": "' + s.call_blanc[i] + '",\n'
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
    tmp = sorted(list(s.all.items()), key=lambda x: x[1][0])
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

    data = '"node":\n'
    data += '[\n'

    width = 4

    tmp = []
    for n in s.node_list:
        tmp.append(n)
    node_list = sorted(tmp)

    #node_list = sorted(node_list, key=lambda x: x[-1])

    total = len(node_list)
    line = int(total / width)

    complete = total - (line * width)

    if complete != 0:
        line += 1
        complete = (line * width) - total
        for n in range(0, complete):
            node_list.append('')

    limit = len(node_list)
    indice = 0

    while(indice < limit):
        data += '{\n'
        for e in range(0, width - 1):
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
    tmp = sorted(list(s.porteuse.items()), key=lambda x: x[1])
    tmp.reverse()

    data = '"porteuse":\n'

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
    tmp = sorted(list(s.tot.items()), key=lambda x: x[1])
    tmp.reverse()

    data = '"tot":\n'

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
    tmp = sorted(list(s.all.items()), key=lambda x: convert_time_to_second(x[1][1]))
    tmp.reverse()

    data = '"all":\n'

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

        for e in range(2, limit, 2):
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

# Log all
def log_all_tiny():
    tmp = sorted(list(s.all.items()), key=lambda x: convert_time_to_second(x[1][1]))
    tmp.reverse()

    data = '"all":\n'

    data += '[\n'

    p = 1
    for c, t in tmp:
        data += '{\n'
        data += '\t"Pos": "' + str('{:0>3d}'.format(int(p))) + '",\n'
        data += '\t"Indicatif": "' + c + '",\n'
        data += '\t"TX": ' + str(t[0]) + ',\n'
        data += '\t"Durée": "' + str(t[1]) + '"\n'
        data += '},\n'

        p += 1
        if p > 10:
            break

    if p > 1:
        last = data.rfind(',')
        data = data[:last] + '' + data[last + 1:]

    data += ']\n'

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

    tot = []
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

                # TOT
                search_start = content.find('TOT": ')               # Search this pattern
                search_start += 6                                   # Shift...
                search_stop = content.find(',', search_start)       # And close it...

                tmp = content[search_start:search_stop]

                tot.append(tmp)

                # Emission cumulée

                search_start = content.find('Emission cumulée": "') # Search this pattern
                search_start += 20                                  # Shift...
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
                search_start = content.find('Links actifs": ')      # Search this pattern
                search_start += 15                                  # Shift...
                search_stop = content.find(',', search_start)       # And close it...

                tmp = content[search_start:search_stop]

                actif.append(tmp)

                # Noeuds connectés
                search_start = content.find('Links connectés": ')   # Search this pattern
                search_start += 18                                  # Shift...
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
        data += '\t"' + room + '": ' + tx[tmp] + ',\n'
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

    data += '\t"Scanner RRF": "Links actifs",\n'
    tmp = 0
    for room in room_other:
        data += '\t"' + room + '": ' + actif[tmp] + ',\n'
        tmp += 1

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '}, \n'
    data += '{\n'

    data += '\t"Scanner RRF": "Links connectés",\n'
    tmp = 0
    for room in room_other:
        data += '\t"' + room + '": ' + connected[tmp] + ',\n'
        tmp += 1

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '}, \n'
    data += '{\n'

    data += '\t"Scanner RRF": "TOT",\n'
    tmp = 0

    for room in room_other:
        data += '\t"' + room + '": ' + tot[tmp] + ',\n'
        tmp += 1

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    data += '}\n'
    data += '],\n'

    return data

# Log abstract
def log_type():

    total = len(s.node_list)
    data_a = ''
    data_b = ''

    data = '"type":\n'
    data += '[\n'
    data += '{\n'


    for t in [' H', ' V', ' U', ' R', ' T', ' T10M', ' 10M', ' 6M']:
        size = len(t)
        tmp = 0
        for n in s.node_list:
            if n[-size:] == t:
                tmp += 1
        data_a += '\t"' + t.strip() +'": ' + str(tmp) + ',\n'
        if total != 0:
            percent = (float(tmp) / total) * 100
            percent = "{0:.2f}".format(percent)
            data_b += '\t"' + t.strip() +'": "' + str(percent) + ' %",\n'
       
    data += data_a

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    if total != 0:
        data += '},\n'
        data += '{\n'
        data += data_b

        last = data.rfind(',')
        data = data[:last] + '' + data[last + 1:]

    data += '}\n'
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
            message_node += 'Link entrant : ' + tmp + '. '
        else:
            message_node += 'Links entrants : ' + tmp + '. '

    # Nœuds sortants

    tmp = ''
    for n in s.node_list_out:
        tmp += str(n) + ', '
    tmp = tmp[:-2]

    if tmp != '':
        if len(s.node_list_out) == 1:
            message_node += 'Link sortant : ' + tmp + '. '
        else:
            message_node += 'Links sortants : ' + tmp + '. '

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

    data += ']\n'

    return data

# Log user
def log_user():

    page = ''
    
    try:
        r = requests.get('http://rrf.f5nlg.ovh:8080/server-status', verify=False, timeout=10)
        page = r.content.decode('utf-8')
    except requests.exceptions.ConnectionError as errc:
        print('Error Connecting:', errc)
    except requests.exceptions.Timeout as errt:
        print('Timeout Error:', errt)

    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', page)
    ip = list(set(ip))

    return str(len(ip) - 1)

# Restart
def restart():

    filename = s.log_path + '/' + s.room + '-today/rrf.json'
    if os.path.isfile(filename):
        rrf_json = open(filename)
        rrf_data = rrf_json.read()
        rrf_data = rrf_data.replace('Extended', '') # Fix old format !
        try:
            rrf_data = json.loads(rrf_data)
        except:
            return 0

    # Section activity and abstract

    i = 0
    for data in rrf_data['activity']:
        s.qso_hour[i] = data['TX']
        i += 1

    s.qso = sum(s.qso_hour)

    for data in rrf_data['abstract']:
        s.day_duration = convert_time_to_second(data['Emission cumulée'])

    # Section last

    i = 0
    for data in rrf_data['last']:
        s.call[i] = data['Indicatif']
        s.call_date[i] = data['Heure']
        if 'Blanc' in data:
            s.call_blanc[i] = data['Blanc']
        s.call_time[i] = convert_time_to_second(data['Durée'])
        i += 1

    # Section porteuse

    for data in rrf_data['porteuse']:
        s.porteuse[data['Indicatif']] = [data['TX'], data['Date']]

    # Section tot

    if 'tot' in rrf_data:
        for data in rrf_data['tot']:
            s.tot[data['Indicatif']] = [data['TX'], data['Date']]

    # Section all

    if 'all' in rrf_data:
        for data in rrf_data['all']:
            s.all[data['Indicatif']] = [data['TX'], data['Durée']]

            chrono = data['Chrono'].split(', ')
            heure = data['Heure'].split(', ')

            limit = len(chrono)

            for e in range(limit):
                s.all[data['Indicatif']].append(heure[e])
                s.all[data['Indicatif']].append(chrono[e])

    s.transmit = False

    return 0

def log_iptable():
    data_patrol = []
    new_json = []
    log_count = 0

    try:
        with open(s.patrol_filename) as json_file:
            data_patrol = json.load(json_file)
    except:
        pass

    if len(data_patrol) == 4:
        for serveur in data_patrol:
            for data in data_patrol[serveur]['blockip']:
                if data['Salon'].lower() == s.room.lower():
                    #if data['Admin'] != 'ADMIN':
                    #    data['Admin'] = 'ADMIN (' + data['Admin'] + ')'
                    new_json.append({
                        'Indicatif': data['Indicatif'],
                        'Type': data['Admin'],
                        'Début': data['Date'],
                        'Durée': '-',
                        'Fin': '-'
                    })

            for data in data_patrol[serveur]['sentinel']:
                if s.room.lower() == 'rrf':
                    new_json.append({
                        'Indicatif': data['Indicatif'],
                        'Type': data['Type'],
                        'Début': data['Début'],
                        'Durée': data['Durée'],
                        'Fin': data['Fin']
                    })

        # Si le nouveau flux n'est pas vide et que les 4 serveurs ont répondu
        if (new_json != s.iptable_json):
            s.iptable_json = new_json.copy()

    data = '"iptable":\n'
    data += json.dumps(s.iptable_json)
    data += ',\n'

    return data
     