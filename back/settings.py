#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

# Version

version = '3.0.0'

# Default path

log_path = '/tmp/RRF'       # Log path: Default value !
patrol_filename = '/var/www/RRFTracker/rrf_patrol.json'
api_url = 'http://rrf2.f5nlg.ovh:4440/nodes'

# Set room

room_list = {
    'RRF': {
        'dtmf': '9 6',
        'realname': 'RRF', 
    },
    'TECHNIQUE': {
        'dtmf': '9 8',
        'realname': 'Technique', 
    },
    'INTERNATIONAL': {
        'dtmf': '9 9',
        'realname': 'International', 
    },
    'BAVARDAGE': {
        'dtmf': '1 0 0',
        'realname': 'Bavardage', 
    },
    'LOCAL': {
        'dtmf': '1 0 1',
        'realname': 'Local', 
    },
    'EXPERIMENTAL': {
        'dtmf': '1 0 2',
        'realname': 'Expérimental', 
    },
    'FON': {
        'dtmf': '9 7',
        'realname': 'FON', 
    }
}

log_path_day = {}           # Log path day: Default value !

call = {}                   # Call list
call_date = {}              # Call date list
call_blanc = {}             # Call blanc list
call_time = {}              # Call time list
call_current = {}           # Call current
call_previous = {}          # Call previous

node_list = {}              # Node list
node_list_old = {}          # Node list old
node_list_in = {}           # Node list in
node_list_out = {}          # Node list out
node_count = {}             # Node count
node_count_max = {}         # Node count max
node_count_min = {}         # Node count min

tot = {}                    # TOT dict
tot_start = {}              # TOT start
tot_current = {}            # TOT current
tot_limit = {}              # TOT limit time (02:03 puis 02:33...)

qso = {}                    # QSO
qso_hour = {}               # QSO by hour

transmit = {}               # Detect transmit
porteuse = {}               # Porteuse dict
all = {}                    # All dict
day_duration = {}           # Total emission time
duration = {}               # Duration
stat_save = {}              # If False, stat need to be save
init = {}                   # Initial init
intempestif = {}            # Tuned me !!!

iptable_json = []
whereis_call = {}
whereis_list = {}
whois_list = {}

for r in room_list:
    log_path_day[r] = ''
    call[r] = [''] * 10
    call_date[r] = [''] * 10
    call_blanc[r] = [''] * 10
    call_time[r] = [''] * 10
    call_current[r] = ''
    call_previous[r] = ''

    transmit[r] = 'False'
    all[r] = {}
    porteuse[r] = {}
    intempestif[r] = 2

    tot[r] = {}
    tot_start[r] = ''
    tot_current[r] = ''

    node_list[r] = []
    node_list_old[r] = []
    node_list_in[r] = []
    node_list_out[r] = []
    node_count[r] = 0
    node_count_max[r] = 0
    node_count_min[r] = 10**4

    qso[r] = 0
    qso_hour[r] = [0] * 24

    day_duration[r] = 0
    duration[r] = 0

    tot_limit[r] = '02:33'

    stat_save[r] = False
    init[r] = True

    whereis_call[r] = ''

message_node_old = ''       # Old message node
message_current = ''        # Current message
message_timer = 0           # Timer message
message_timer_limit = 0     # Timer limit message

# Set time and date

hour = ''
minute = ''
seconde = ''
main_loop = .200            # Main loop tempo
