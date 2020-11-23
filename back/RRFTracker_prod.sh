#!/bin/sh

PATH_SCRIPT='/opt/RRFTracker/back/RRFTracker.py'
PATH_MEDIA='/opt/RRFTracker/front/assets'
PATH_HTML='/opt/RRFTracker/front/index.html'

PATH_LOG='/var/www/RRFTracker'
PATH_PID='/tmp'

NOW=$(date +"%H%M%S")

ROOMS=("RRF" "TECHNIQUE" "BAVARDAGE" "LOCAL" "INTERNATIONAL" "EXPERIMENTAL" "FON")

for ROOM in "${ROOMS[@]}"
do
    echo $ROOM
done
