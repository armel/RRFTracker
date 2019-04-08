#!/bin/bash

cd /opt/RRFTracker_Web/
nohup python /opt/RRFTracker_Web/back/RRFTracker.py --room RRF --log-path /var/www/mrtg/RRFTracker/ &
nohup python /opt/RRFTracker_Web/back/RRFTracker.py --room TEC --log-path /var/www/mrtg/RRFTracker/ &
#nohup python /opt/RRFTracker_Web/back/RRFTracker.py --room FON --log-path /var/www/mrtg/RRFTracker/ &