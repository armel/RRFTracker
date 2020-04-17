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
    print '  --path         set path to RRF files (default=/var/www/RRFTracker/)'
    print '  --month        analyse on month (default=current month)'
    print '  --week         analyse on week'
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


# Print console
def print_console(tmp, r):

    i = 1
    print 'Salon\t\tPos\tIndicatif\t\tDéclenchements\t\tDurée\t\tRatio'
    print '-----\t\t---\t---------\t\t--------------\t\t-----\t\t-----'
    for e in tmp:
        print r, '\t',
        if len(r) < 8:
            print '\t',
        print '%03d' % i, 
        print '\t', e[0], '\t',
        if len(e[0]) < 15:
            print '\t',
        print '%03d' % e[1][0],

        print '\t\t\t',
        print convert_second_to_time(e[1][1]),
        print '\t',

        if e[1][2] != 0:
            print '%06.2f' % e[1][2] + ' s/d'
        else:
            print 'Jamais en émission'

        i += 1

    return 0


def main(argv):

    room_list = {
        'RRF',
        'TECHNIQUE',
        'BAVARDAGE',
        'INTERNATIONALE',
        'LOCAL',
        'EXPERIMENTAL',
        'FON'
    }

    porteuse = dict()
    all = dict()
    total = dict()
    full = dict()
    limit = 0

    tmp = datetime.datetime.now()

    search_path = '/var/www/RRFTracker/'
    search_pattern = tmp.strftime('%Y-%m')
    search_type = 'month'

    # Check and get arguments
    try:
        options, remainder = getopt.getopt(argv, '', ['help', 'path=', 'month=', 'week=', 'limit='])
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
        elif opt in ('--limit'):
            limit = int(arg)

    print color.BLUE + 'Path ' + color.END + search_path,
    print ' with ',
    print color.BLUE + 'Pattern ' + color.END + search_pattern,
    print '...'

    time_super_total = 0

    for r in room_list:

        porteuse.clear()
        all.clear()
        total.clear()

        if search_type == 'month':
            path = search_path + r + '-' + search_pattern + '-*/rrf.json'
            file = glob.glob(path)
            file.sort()
        else:
            file = []
            start_date = time.asctime(time.strptime(str(datetime.datetime.today().year) + ' %d 1' % int(search_pattern), '%Y %W %w'))
            start_date = datetime.datetime.strptime(start_date, '%a %b %d %H:%M:%S %Y')
            file = [search_path + 'RRF-' + start_date.strftime('%Y-%m-%d') + '/rrf.json']
            for i in range(1, 7):
                file.append(search_path + 'RRF-' + (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') + '/rrf.json')

        #for f in file:
        #    print f

        time_total = 0

        for f in file:
            if os.path.isfile(f):
                rrf_json = open(f)
                rrf_data = rrf_json.read()
                rrf_data = rrf_data.replace('Extended', '') # Fix old format !
                try:
                    rrf_data = json.loads(rrf_data)

                    for data in rrf_data['porteuse']:
                        try:
                            porteuse[data[u'Indicatif'].encode('utf-8')] += data[u'TX']
                        except:
                            porteuse[data[u'Indicatif'].encode('utf-8')] = data[u'TX']

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

        if 'RRF' in porteuse:
            del porteuse['RRF']
        if 'F5ZIN-L' in porteuse:
            del porteuse['F5ZIN-L']

        tmp = sorted(porteuse.items(), key=lambda x: x[1])
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

        # Affichage

        print '===================='
        print color.BLUE + r + color.END
        print '===================='

        print color.BLUE + r + ' - Classement par déclenchements' + color.END
        print
        tmp = sorted(total.items(), key=lambda x: x[1][0])
        tmp.reverse()
        print_console(tmp, r)
        print '----------'

        print color.BLUE + r + ' - Classement par ratio' + color.END
        print
        tmp = sorted(total.items(), key=lambda x: x[1][2])
        tmp.reverse()
        print_console(tmp, r)
        print '----------'

        print color.BLUE + r + ' - Classement par durée' + color.END
        print
        tmp = sorted(total.items(), key=lambda x: x[1][1])
        tmp.reverse()
        print_console(tmp, r)
        print '----------'

        # Synthese

        somme = []
        link = []
        somme_intempestif = 0

        for e in tmp:
            if e[1][1] < 600:
                somme.append(e[1][0]) 
                link.append(e[0])

            somme_intempestif += e[1][0]

        print 'Remarque :'
        print len(somme), 'links ont généré moins de 10 minutes de BF dans le mois pour', sum(somme), 'déclenchements !'
        for l in link:
            print l,
        print

        print '----------'

        print 'Total des déclenchements :', somme_intempestif

    print '----------'
    print 'Classement des links les plus actifs tous salons confondus (hors FON)'
    print '----------'

    tmp = sorted(full.items(), key=lambda x: x[1], reverse=True)
    i = 1

    for e in tmp:
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
