#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFTracker version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

# Version

version = '1.3.2'

# Default room and path

room = 'RRF'			# Room: Default value !
log_path = '/tmp/RRF'	# Log path: Default value !

# Set call

call = ['', '', '', '', '', '', '', '', '', '']     	# Call list
call_date = ['', '', '', '', '', '', '', '', '', '']  	# Call date list
call_time = ['', '', '', '', '', '', '', '', '', '']  	# Call time list
call_current = call[0]                                	# Call current
call_previous = call[1]                               	# Call previous

qso = 0					# QSO count
qso_hour = [0] * 24		# QSO list for histogramm
node_count = 0			# Node count
day_duration = 0		# Total emission time

node = dict()			# Node dict
porteuse = dict()    	# Porteuse dict

transmit = True			# Detect transmit
stat_save = False		# If False, stat need to be save

# Set time and date

tot_start = ''
tot_current = ''
hour = ''
minute = ''
seconde = ''
duration = 0
