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
import json

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
    print '  --path        set path to RRF files (default=/var/www/RRFTracker/)'
    print '  --days        number of last days to analyse  (default=0 for today only)'
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

    room_list = {
        'RRF',
        'TECHNIQUE',
        'BAVARDAGE',
        'INTERNATIONAL',
        'LOCAL',
        'EXPERIMENTAL',
        'FON'
    }

    tx = dict()
    all = dict()
    total = dict()
    full = dict()
    limit = 0

    tmp = datetime.datetime.now()

    search_path = '/var/www/RRFTracker/'
    search_pattern = 1
    search_type = 'month'

    # Check and get arguments
    try:
        options, remainder = getopt.getopt(argv, '', ['help', 'path=', 'days='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in options:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt in ('--path'):
            search_path = arg
        elif opt in ('--days'):
            search_pattern = int(arg)
            search_type = 'days'

    print color.BLUE + 'Path ' + color.END + search_path,
    print ' with ',
    print color.BLUE + 'Pattern ' + color.END + str(search_pattern),
    print '...'

    search_pattern -= 1
    time_super_total = 0

    for r in room_list:

        tx.clear()
        all.clear()
        total.clear()

        file = []
        start_date = datetime.datetime.now() - datetime.timedelta(search_pattern)
        file = [search_path + r + '-' + start_date.strftime('%Y-%m-%d') + '/rrf.json']
        for i in range(1, search_pattern + 1):
            file.append(search_path + r + '-' + (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') + '/rrf.json')
 
        time_total = 0

        for f in file:
            #print f
            if os.path.isfile(f):
                rrf_json = open(f)
                rrf_data = rrf_json.read()
                rrf_data = rrf_data.replace('Extended', '') # Fix old format !
                try:
                    rrf_data = json.loads(rrf_data)

                    #print f
                    for data in rrf_data['all']:
                        try:
                            tx[data[u'Indicatif'].encode('utf-8')] += data[u'TX']
                        except:
                            tx[data[u'Indicatif'].encode('utf-8')] = data[u'TX']

                    if 'all' in rrf_data:
                        for data in rrf_data['all']:
                            try:
                                all[data[u'Indicatif'].encode('utf-8')] += convert_time_to_second(data[u'Durée'])
                            except:
                                all[data[u'Indicatif'].encode('utf-8')] = convert_time_to_second(data[u'Durée'])

                    else:
                        for data in rrf_data['all']:
                            try:
                                all[data[u'Indicatif'].encode('utf-8')] += convert_time_to_second(data[u'Durée'])
                            except:
                                all[data[u'Indicatif'].encode('utf-8')] = convert_time_to_second(data[u'Durée'])
                except:
                    pass

        if 'RRF' in tx:
            del tx['RRF']
        if 'F5ZIN-L' in tx:
            del tx['F5ZIN-L']

        tmp = sorted(tx.items(), key=lambda x: x[1])
        tmp.reverse()

        i = 1
        for e in tmp:
            if e[0] in all:
                ratio = (int(all[e[0]]) / float(e[1]))
            else:
                ratio = 0

            if e[0] in all:
                total[e[0]] = [e[1], all[e[0]], ratio]
            else:
                total[e[0]] = [e[1], 0, 0]

            i += 1
            if limit != 0:
                if i > limit:
                    break

        # Calcul du total

        if r != 'FON':
            for a in total:
                if a in full:
                    full[a] += total[a][1]
                else:
                    full[a] = total[a][1]

    print '----------'
    print 'Classement des links les plus actifs tous salons confondus (hors FON)'
    print '----------'

    tmp = sorted(full.items(), key=lambda x: x[1], reverse=True)
    i = 1

    for e in tmp:
        check = e[0].split(' ')
        if len(check) == 3:
            print '%03d' % i, '\t',
            print e[0], '\t\t',
            if len(e[0]) < 7:
                print '\t',
            if len(e[0]) < 15:
                print '\t',
            print convert_second_to_time(e[1])
            i += 1

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
