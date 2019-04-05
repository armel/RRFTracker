#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

import os
from math import cos, asin, sqrt, ceil


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
    if call in history:
        history[call] += 1
    else:
        history[call] = 1

    return history


# Log write for history
def log_write(log_path, day, room, qso_hour, history, call, call_time):

    log_path = log_path + '/' + room + '-' + day

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_history(log_path, qso_hour)
    log_last(log_path, call, call_time)
    log_best(log_path, history)

    return 0

# Log history

def log_history(log_path, qso_hour):

    data = '[\n'

    l = 1
    for i in xrange(0, 24):

        x = str('{:0>2d}'.format(int(i)))
        y = str('{:0>2d}'.format(int(l)))
        z = str('{:0>2d}'.format(qso_hour[i]))

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

# Log best

def log_best(log_path, history):
    tmp = sorted(history.items(), key=lambda x: x[1])
    tmp.reverse()

    print tmp

    data = '[\n'

    p = 1
    for c, t in tmp:
        print c, t
        data += '{\n'
        data += '\t"Call": "' + c + '",\n'
        data += '\t"TX": ' + t + '\n'
        data += '},\n'

        p += 1
        if p > 20:
            break

    data += ']\n'

    last = data.rfind(',')
    data = data[:last] + '' + data[last + 1:]

    file = open(log_path + '/' + 'best.json', 'w')
    file.write(data)
    file.close()

    return 0