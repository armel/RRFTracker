#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

import os
import datetime
import locale

# Usage
def usage():
    print 'Usage: RRFTracker.py [options ...]'
    print
    print '--help               this help'
    print
    print 'Room settings:'
    print '  --room ROOM        set room (default=RRF, choose between [RRF, TEC, FON])'
    print
    print 'Log settings:'
    print '  --log-path         set the location of log files'
    print
    print '88 & 73 from F4HWN Armel'

# Convert time in second to minute
def convert_time(time):
    hours = time // 3600
    time = time - (hours * 3600)

    minutes = time // 60
    seconds = time - (minutes * 60)

    if hours == 0:
        return str('{:0>2d}'.format(int(minutes))) + ':' + str('{:0>2d}'.format(int(seconds)))
    else:
        return str('{:0>2d}'.format(int(hours))) + ':' + str('{:0>2d}'.format(int(minutes))) + ':' + str('{:0>2d}'.format(int(seconds)))

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

# Log write for history
def log_write(log_path, day, room, qso_hour, node, porteuse, call, call_date, call_time, node_count, node_count_max, node_count_min, duration, call_current, tot):

    log_path_day = log_path + '/' + room + '-' + day

    if not os.path.exists(log_path_day):
        os.makedirs(log_path_day)
        os.popen('cp /opt/RRFTracker_Web/front/index.html ' + log_path_day + '/index.html')
        os.popen('ln -sfn ' + log_path_day + ' ' + log_path + '/' + room + '-today')

    log_transmit(log_path_day, call_current, tot)
    log_abstract(log_path_day, room, qso_hour, node, node_count, node_count_max, node_count_min, duration)
    log_history(log_path_day, qso_hour)
    log_last(log_path_day, call, call_date, call_time)
    log_node(log_path_day, node, 'best')
    log_node(log_path_day, node, 'all')
    log_porteuse(log_path_day, porteuse, 'porteuse')
    log_porteuse(log_path_day, porteuse, 'porteuse_extended')

    return 0

# Log abstract
def log_abstract(log_path, room, qso_hour, history, node, node_max, node_min, tx):

    data = '[\n'

    locale.setlocale(locale.LC_TIME, '')

    tmp = datetime.datetime.now()
    now = tmp.strftime(' du %A %d/%m/%Y à %H:%M')

    data += '{\n'
    data += '\t"Salon": "' + room + '",\n'
    data += '\t"Date": "' + now + '",\n'
    data += '\t"TX total": ' + str(sum(qso_hour)) + ',\n'
    data += '\t"Emission cumulée": "' + convert_time(tx) + '",\n'
    data += '\t"Nœuds actifs": ' + str(len(history)) + ',\n'
    data += '\t"Nœuds connectés": ' + str(node) + ',\n'
    data += '\t"Nœuds max": ' + str(node_max) + ',\n'
    data += '\t"Nœuds min": ' + str(node_min) + '\n'
    data += '},\n'

    data += ']\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    file = open(log_path + '/' + 'abstract.json', 'w')
    file.write(data)
    file.close()

    return 0

# Log transmit
def log_transmit(log_path, call_current, tot):

    if tot == 0:
        call_current = ''

    if call_current == '':
        call_current = 'Waiting TX'
        tot = 0

    data = '[\n'

    data += '{\n'
    data += '\t"Indicatif": "' + call_current + '",\n'
    data += '\t"TOT": ' + str(tot) + '\n'
    data += '},\n'

    data += ']\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    file = open(log_path + '/' + 'transmit.json', 'w')
    file.write(data)
    file.close()

    return 0

# Log history
def log_history(log_path, qso_hour):

    data = '[\n'

    l = 1
    for i in xrange(0, 24):

        x = str('{:0>2d}'.format(int(i)))
        y = str('{:0>2d}'.format(int(l)))
        z = str(qso_hour[i])

        x += 'h - ' + y + 'h'

        l += 1

        if l == 24:
            l = 0

        data += '{\n'
        data += '\t"Hour": "' + x + '",\n'
        data += '\t"TX": ' + z + '\n'
        data += '},\n'

    data += ']\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    file = open(log_path + '/' + 'activity.json', 'w')
    file.write(data)
    file.close()

    return 0

# Log last
def log_last(log_path, call, call_date, call_time):

    data = '[\n'

    for i in xrange(0, 10):
        if call_date[i] == '':
            break
        data += '{\n'
        data += '\t"Date": "' + call_date[i] + '",\n'
        data += '\t"Indicatif": "' + call[i] + '",\n'
        data += '\t"Durée": "' + convert_time(call_time[i]) + '"\n'
        data += '},\n'

    data += ']\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    file = open(log_path + '/' + 'last.json', 'w')
    file.write(data)
    file.close()

    return 0

# Log node
def log_node(log_path, node, type):
    tmp = sorted(node.items(), key=lambda x: x[1])
    tmp.reverse()

    if type == 'best':
        limit = 20
    else:
        limit = 10**4

    data = '[\n'

    p = 1
    for c, t in tmp:
        data += '{\n'
        if type in ['all']:
            data += '\t"Pos": "' + str('{:0>3d}'.format(int(p))) + '",\n'
        data += '\t"Indicatif": "' + c + '",\n'
        if type in ['all']:
            data += '\t"Durée": "' + convert_time(t[1]) + '",\n'
        data += '\t"TX": ' + str(t[0]) + '\n'
        data += '},\n'

        p += 1
        if p > limit:
            break

    data += ']\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    file = open(log_path + '/' + type + '.json', 'w')
    file.write(data)
    file.close()

    return 0

# Log special
def log_porteuse(log_path, node, type):
    tmp = sorted(node.items(), key=lambda x: x[1])
    tmp.reverse()

    data = '[\n'

    p = 1
    for c, t in tmp:
        if type == 'porteuse':
            if t[0] < 10:
                break

        data += '{\n'
        if type == 'porteuse':
            data += '\t"Pos": "' + str('{:0>3d}'.format(int(p))) + '",\n'
            data += '\t"Indicatif": "' + c + '",\n'
            data += '\t"TX": ' + str(t[0]) + '\n'
        else:
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

    data += ']\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    file = open(log_path + '/' + type + '.json', 'w')
    file.write(data)
    file.close()

    return 0
