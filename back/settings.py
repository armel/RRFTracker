#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

# Version

version = '2.7.5'

# Default room and path

room = 'RRF'                # Room: Default value !
log_path = '/tmp/RRF'       # Log path: Default value !
log_path_day = ''           # Log path day: Default value !

# Set call

call = [''] * 10            # Call list
call_date = [''] * 10       # Call date list
call_blanc = [''] * 10      # Call blanc list
call_time = [''] * 10       # Call time list
call_current = call[0]      # Call current
call_previous = call[1]     # Call previous

qso = 0                 	# QSO count
qso_hour = [0] * 24     	# QSO list for histogramm
node_count = 0          	# Node count
node_count_max = 0      	# Node count max
node_count_min = 10**4  	# Node count min
user_count = 0              # User count

node_list = []          	# Node list
node_list_old = []      	# Node list
node_list_in = []       	# Node list in
node_list_out = []      	# Node list out

day_duration = 0        	# Total emission time

porteuse = {}               # Porteuse dict
all = {}                    # All dict
tot = {}                    # TOT dict
tot_limit = '02:33'         # TOT limit time (02:03 puis 02:33...)

transmit = True         	# Detect transmit
stat_save = False       	# If False, stat need to be save

message_node_old = ''       # Old message node
message_current = ''        # Current message
message_timer = 0           # Timer message
message_timer_limit = 0     # Timer limit message

iptable_json = []           # IP stream
whereis_list = {}           # Whereis dict
whois_list = {}             # Whois dict

# Set time and date

tot_start = ''
tot_current = ''
hour = ''
minute = ''
seconde = ''
duration = 0
intempestif = 2             # Tuned me !!!
main_loop = .200            # Main loop tempo

# Set init

init = True                 # Check if init...

# Set url and path

rrf1 = 'http://217.182.206.155'
rrf2 = 'http://51.210.177.28'

room_list = {
    'RRF': {
        'url': rrf1 + '/api/svxlink/RRF',
        'dtmf': '9 6',
    },
    'TECHNIQUE': {
        'url': rrf1 + '/api/svxlink/technique',
        'dtmf': '9 8',
    },
    'INTERNATIONAL': {
        'url': rrf1 + '/api/svxlink/international',
        'dtmf': '9 9',
    },
    'BAVARDAGE': {
        'url': rrf1 + '/api/svxlink/bavardage',
        'dtmf': '1 0 0',
    },
    'LOCAL': {
        'url': rrf1 + '/api/svxlink/local',
        'dtmf': '1 0 1',
    },
    #'EXPERIMENTAL': {
    #    'url': rrf1 + '/api/svxlink/experimental',
    #    'dtmf': '1 0 2',
    #},
    'FON': {
        'url': rrf1 + '/api/svxlink/FON',
        'dtmf': '9 7',
    }
}

patrol_filename = '/var/www/RRFTracker/rrf_patrol.json'
whereis_api = rrf2 + ':4440/nodes'
