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
    print 'I2C settings:'
    print '  --i2c-port         set i2c port (default=0)'
    print '  --i2c-address      set i2c address (default=0x3C)'
    print
    print 'Display settings:'
    print '  --display          set display (default=sh1106, choose between [sh1106, ssd1306])'
    print '  --display-width    set display width (default=128)'
    print '  --display-height   set display height (default=64)'
    print
    print 'Room settings:'
    print '  --room ROOM        set room (default=RRF, choose between [RRF, TEC, FON])'
    print
    print 'WGS84 settings:'
    print '  --latitude         set latitude (default=48.8483808, format WGS84)'
    print '  --longitude        set longitude (default=2.2704347, format WGS84)'
    print
    print 'Log settings:'
    print '  --log              enable log'
    print
    print '88 & 73 from F4HWN Armel'


# Save stats to get most active link
def save_stat(history, call):
    if call != '':
        if call in history:
            history[call] += 1
        else:
            history[call] = 1

    return history


# Log write for history
def log_write(log_path, day, room, qso_hour, history, call, call_time, node, call_current, tot):

    log_path = log_path + '/' + room + '-' + day

    if not os.path.exists(log_path):
        os.makedirs(log_path)
        os.popen('cp /opt/RRFTracker_Web/front/index.html ' + log_path + '/index.html')

    log_transmit(log_path, call_current, tot)
    log_abstract(log_path, room, qso_hour, history, node)
    log_history(log_path, qso_hour)
    log_last(log_path, call, call_time)
    log_node(log_path, history, 'best')
    log_node(log_path, history, 'all')

    return 0

# Log abstract

def log_abstract(log_path, room, qso_hour, history, node):

    data = '[\n'

    tmp = datetime.datetime.now()
    now = tmp.strftime('%d-%m-%Y %H:%M')

    data += '{\n'
    data += '\t"Salon": "' + room + '",\n'
    data += '\t"Date": "' + now + '",\n'
    data += '\t"TX total": ' + str(sum(qso_hour)) + ',\n'
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

def log_last(log_path, call, call_time):

    data = '[\n'

    for i in xrange(0, 10):
        if call_time[i] == '':
            break
        data += '{\n'
        data += '\t"Date": "' + call_time[i] + '",\n'
        data += '\t"Call": "' + call[i] + '"\n'
        data += '},\n'

    data += ']\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    file = open(log_path + '/' + 'last.json', 'w')
    file.write(data)
    file.close()

    return 0

# Log node

def log_node(log_path, history, type):
    tmp = sorted(history.items(), key=lambda x: x[1])
    tmp.reverse()

    if type == 'best':
        limit = 20
    else:
        limit = 10**4

    data = '[\n'

    p = 1
    for c, t in tmp:
        data += '{\n'
        if type == 'all':
            data += '\t"Pos": "' + str('{:0>3d}'.format(int(p))) + '",\n'
        data += '\t"Call": "' + c + '",\n'
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