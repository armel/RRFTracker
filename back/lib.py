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
def save_stat(history, call, duration=0):
    if duration == 0:
        if call != '':
            if call in history:
                history[call] += 1
            else:
                history[call] = 1
    elif isinstance(duration, int) and duration < 600:
        if call != '':
            if call in history:
                history[call] += duration
            else:
                history[call] = duration
    else:
        if call != '':
            try:
                history[call].append(duration)
            except KeyError:
                history[call] = [duration]

    return history

# Log write for history
def log_write(log_path, day, room, qso_hour, node_tx, node_duration, porteuse_tx, porteuse_time, call, call_date, call_time, node, duration, call_current, tot):

    log_path_day = log_path + '/' + room + '-' + day

    if not os.path.exists(log_path_day):
        os.makedirs(log_path_day)
        os.popen('cp /opt/RRFTracker_Web/front/index.html ' + log_path_day + '/index.html')
        os.popen('ln -sfn ' + log_path_day + ' ' + log_path + '/' + room + '-today')

    log_transmit(log_path_day, call_current, tot)
    log_abstract(log_path_day, room, qso_hour, node_tx, node, duration)
    log_history(log_path_day, qso_hour)
    log_last(log_path_day, call, call_date, call_time)
    log_node(log_path_day, node_tx, node_duration, 'best')
    log_node(log_path_day, node_tx, node_duration, 'all')
    log_node(log_path_day, porteuse_tx, porteuse_time, 'porteuse')
    log_special(log_path_day, porteuse_time, 'porteuse_time')

    return 0

# Log abstract
def log_abstract(log_path, room, qso_hour, history, node, tx):

    data = '[\n'

    tmp = datetime.datetime.now()
    now = tmp.strftime('%d-%m-%Y %H:%M')

    data += '{\n'
    data += '\t"Salon": "' + room + '",\n'
    data += '\t"Date": "' + now + '",\n'
    data += '\t"TX total": ' + str(sum(qso_hour)) + ',\n'
    data += '\t"Durée émission": "' + convert_time(tx) + '",\n'
    data += '\t"Noeuds actifs": ' + str(len(history)) + ',\n'
    data += '\t"Noeuds total": ' + str(node) + '\n'
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
    data += '\t"Node": "' + call_current + '",\n'
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
        data += '\t"Call": "' + call[i] + '",\n'
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
def log_node(log_path, node, complement, type):
    tmp = sorted(node.items(), key=lambda x: x[1])
    tmp.reverse()

    if type == 'best':
        limit = 20
    else:
        limit = 10**4

    data = '[\n'

    p = 1
    for c, t in tmp:
        if type in ['porteuse']:
            if t < 10:
                break
        data += '{\n'
        if type in ['all', 'porteuse']:
            data += '\t"Pos": "' + str('{:0>3d}'.format(int(p))) + '",\n'
        data += '\t"Call": "' + c + '",\n'
        if type in ['all']:
            if c in complement:
                data += '\t"Durée": "' + convert_time(complement[c]) + '",\n'
            else:
                data += '\t"Durée": "' + convert_time(0) + '",\n'
        data += '\t"TX": ' + str(t) + '\n'
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
def log_special(log_path, node, type):
    data = ''
    for c in node:
        data += c + '\n'
        for t in node[c]:
            data += '\t' + t + '\n'

    file = open(log_path + '/' + type + '.log', 'w')
    file.write(data)
    file.close()

    return 0