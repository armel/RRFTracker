#!/bin/bash

rm -rf /var/www/RRFTracker/RRF*
rm -rf /var/www/RRFTracker/TEC*
cd /opt/RRFTracker_Web/
nohup python /opt/RRFTracker_Web/back/RRFTracker.py --room RRF --log-path /var/www/RRFTracker &
nohup python /opt/RRFTracker_Web/back/RRFTracker.py --room TEC --log-path /var/www/RRFTracker &
