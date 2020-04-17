#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

import os
import glob
import datetime
import time
import sys
import getopt


# Ansi color
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Usage
def usage():
    print 'Usage: RRFTracker.py [options ...]'
    print
    print '--help               this help'
    print
    print 'Search settings:'
    print '  --path         set path to RRF files (default=/var/www/RRFTracker/)'
    print '  --month        set search month (default=current month)'
    print '  --week         set search week (default=current week)'
    print '  --format       set output format (default=text, json)'
    print
    print '88 & 73 from F4HWN Armel'

# Convert second to time
def convert_second_to_time(time):
    hours = time // 3600
    time = time - (hours * 3600)

    minutes = time // 60
    seconds = time - (minutes * 60)

    if hours == 0:
        return str('{:0>2d}'.format(int(minutes))) + 'm ' + str('{:0>2d}'.format(int(seconds))) + 's'
    else:
        return str('{:0>2d}'.format(int(hours))) + 'h ' + str('{:0>2d}'.format(int(minutes))) + 'm ' + str('{:0>2d}'.format(int(seconds))) + 's'


# Convert time to second
def convert_time_to_second(time):
    if len(time) > 5:
        format = [3600, 60, 1]
    else:
        format = [60, 1]

    return sum([a * b for a, b in zip(format, map(int, time.split(':')))])

def main(argv):

    room_list = [
        'RRF',
        'TECHNIQUE',
        'INTERNATIONAL',
        'BAVARDAGE',
        'LOCAL',
        #'EXPERIMENTAL',
        'FON'
    ]

    tmp = datetime.datetime.now()

    search_path = '/var/www/RRFTracker/'
    search_pattern = tmp.strftime('%Y-%m')
    search_type = 'month'
    search_format = 'text'

    # Check and get arguments
    try:
        options, remainder = getopt.getopt(argv, '', ['help', 'path=', 'month=', 'week='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in options:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt in ('--path'):
            search_path = arg
        elif opt in ('--month'):
            search_pattern = arg
            search_type = 'month'
        elif opt in ('--week'):
            search_pattern = arg
            search_type = 'week'

    print color.BLUE + 'Path ' + color.END + search_path,
    print ' with ',
    print color.BLUE + 'Pattern ' + color.END + search_pattern,
    print '...'

    time_total = {}

    for r in room_list:
        print color.BLUE + r + color.END
        print
        if search_type == 'month':
            path = search_path + r + '-' + search_pattern + '-*/rrf.json'
            file = glob.glob(path)
            file.sort()
        else:
            file = []
            start_date = time.asctime(time.strptime(datetime.datetime.today().year + ' %d 1' % int(search_pattern), '%Y %W %w'))
            start_date = datetime.datetime.strptime(start_date, '%a %b %d %H:%M:%S %Y')
            file = [search_path + r + '-' + start_date.strftime('%Y-%m-%d') + '/rrf.json']
            for i in range(1, 7):
                file.append(search_path + r + '-' + (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') + '/rrf.json')

        for f in file:
            tmp = f.split('/')
            tmp = tmp[-2]
            tmp = tmp.split('-')
            d = tmp[1] + '-' + tmp[2] + '-' + tmp[3]

            try:
                time_total[d][r] = {}
            except:
                time_total[d] = {}

            if os.path.isfile(f):
                with open(f, 'r') as content_file:
                    content = content_file.read()

                    # Indicatif

                    search_start = content.find('Emission cumulée": "') # Search this pattern
                    search_start += 21                                  # Shift...
                    search_stop = content.find('"', search_start)       # And close it...

                    print d, ':', convert_second_to_time(convert_time_to_second(content[search_start:search_stop]))

                    try:
                        time_total[d][r] += convert_time_to_second(content[search_start:search_stop])
                    except:
                        time_total[d][r] = convert_time_to_second(content[search_start:search_stop])


        tmp = 0
        for d in time_total:
            try:
                tmp += time_total[d][r]
            except:
                pass
        if r == 'FON':
            tmp_fon = tmp

        print 'Total :', convert_second_to_time(tmp)

        print '----------'

    print 'Classement SANS le FON'
    print
    day = dict()

    for d in time_total:
        tmp = 0
        for r in room_list:
            if r != 'FON':
                try:
                    tmp += time_total[d][r]
                except:
                    pass
        day[d] = tmp
 
    day = sorted(day.items(), key=lambda x: x[1], reverse=True)

    for k, v in day:
        print k, ':', convert_second_to_time(v)

    print '----------'

    print 'Classement AVEC le FON'
    print
    day = dict()

    for d in time_total:
        tmp = 0
        for r in room_list:
            try:
                tmp += time_total[d][r]
            except:
                pass
        day[d] = tmp
 
    day = sorted(day.items(), key=lambda x: x[1], reverse=True)

    for k, v in day:
        print k, ':', convert_second_to_time(v)


    print '----------'

    tmp = 0
    for d in time_total:
        for r in room_list:
            try:
                tmp += time_total[d][r]
            except:
                pass

    print 'Total cumulée :', convert_second_to_time(tmp - tmp_fon), 
    print '(', convert_second_to_time(tmp), 'avec le FON )'


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
