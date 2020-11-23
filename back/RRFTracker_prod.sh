#!/bin/sh

PATH_SCRIPT='/opt/RRFTracker/back/RRFTracker.py'
PATH_MEDIA='/opt/RRFTracker/front/assets'
PATH_HTML='/opt/RRFTracker/front/index.html'

PATH_LOG='/var/www/RRFTracker'
PATH_PID='/tmp'

NOW=$(date +"%H%M%S")

ROOMS=("RRF" "TECHNIQUE" "BAVARDAGE" "LOCAL" "INTERNATIONAL" "EXPERIMENTAL" "FON")

case "$1" in
    start)
        for ROOM in "${ROOMS[@]}"
        do
            cp -a $PATH_MEDIA $PATH_LOG
            echo "Init RRFTracker: $ROOM"
            cp $PATH_HTML $PATH_LOG/RRF-today
            cp ${PATH_LOG}/${ROOM}-today/rrf.json ${PATH_LOG}/${ROOM}-today/rrf_${NOW}.json
        done
        echo "Starting RRFTracker"
        nohup python3 $PATH_SCRIPT --log-path $PATH_LOG > $PATH_PID/RRFTrackerlog 2>&1 & echo $! > $PATH_PID/RRFTracker.pid
        ;;
    stop) 
        echo "Stopping RRFTracker"
        kill `cat $PATH_PID/RRFTracker.pid`
        ;;
esac