#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

import requests
import re
import time

chrono_start = time.time()


# Request HTTP datas
try:
    r = requests.get('http://rrf.f5nlg.ovh:8080/server-status', verify=False, timeout=10)
    page = r.content
except requests.exceptions.ConnectionError as errc:
    print ('Error Connecting:', errc)
except requests.exceptions.Timeout as errt:
    print ('Timeout Error:', errt)

ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', page)
ip = list(set(ip))

total = str(len(ip))

data = '[\n'
data += '{\n'
data += '\t"IP": "' + total + '"\n'
data += '}\n'
data += ']\n'

print data

chrono_stop = time.time()
chrono_time = chrono_stop - chrono_start

print chrono_time
