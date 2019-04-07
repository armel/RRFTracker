#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

# Version

version = '1.1.0'

# Default room

room = 'RRF'                                # Default value !

# Set call

call = ['', '', '', '', '', '', '', '', '', '']       # Call list
call_date = ['', '', '', '', '', '', '', '', '', '']  # Call date list
call_time = ['', '', '', '', '', '', '', '', '', '']  # Call time list
call_current = call[0]                                # Call current
call_previous = call[1]                               # Call previous


blanc = True                                # Detect blank

qso = 0                                     # QSO count
qso_hour = [0] * 24                         # QSO list for histogramm
transmit = True                             # Detect transmit
node = 0                                    # Node count

history = dict()                            # History dict

# Set time and date

timestamp_start = ''
tot_start = ''
tot_current = ''
duration = 0
hour = ''
minute = ''
seconde = ''

# Set log
stat = False								# If False, stat need to be save
log = False                              	# If True, write log
log_path = '/var/www/RRF'					# Log path
