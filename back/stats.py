#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

import os
import glob


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

room_list = {
    'RRF',
    'TECHNIQUE',
    'INTERNATIONAL',
    'BAVARDAGE',
    'LOCAL'
}

for r in room_list:

    print r
    path = '/Users/armel/Sites/RRF/' + r + '-2019-05-*/abstract.json'
    file = glob.glob(path)
    time_total = 0

    for f in file:
        if os.path.isfile(f):
            with open(f, 'r') as content_file:
                content = content_file.read()

                # Indicatif 

                search_start = content.find('Emission cumulée": "') # Search this pattern
                search_start += 21                                  # Shift...
                search_stop = content.find('"', search_start)       # And close it...

                print f, '-->', content[search_start:search_stop]

                time_total += convert_time_to_second(content[search_start:search_stop])

    print 'Total:', convert_second_to_time(time_total)

