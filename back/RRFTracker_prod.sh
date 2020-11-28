#!/bin/bash

PATH_SCRIPT='/opt/RRFTracker/back/RRFTracker.py'
PATH_MEDIA='/opt/RRFTracker/front/assets'
PATH_HTML='/opt/RRFTracker/front/index.html'

PATH_LOG='/var/www/RRFTracker'
PATH_PID='/tmp'

NOW=$(date +"%H%M%S")

ROOMS=("RRF" "TECHNIQUE" "BAVARDAGE" "LOCAL" "INTERNATIONAL" "EXPERIMENTAL" "FON")

case "$1" in
    start)
        cp -a ${PATH_MEDIA} ${PATH_LOG}
        for ROOM in "${ROOMS[@]}"
        do
            echo "Starting RRFTracker: ${ROOM}"
            cp ${PATH_HTML} ${PATH_LOG}/${ROOM}-today
            cp ${PATH_LOG}/${ROOM}-today/rrf.json ${PATH_LOG}/${ROOM}-today/rrf_${NOW}.json
            nohup python3 ${PATH_SCRIPT} --room ${ROOM} --log-path ${PATH_LOG} > ${PATH_PID}/RRFTracker_${ROOM}.log 2>&1 & echo $! > ${PATH_PID}/RRFTracker_${ROOM}.pid
        done
        ;;
    stop)
        for ROOM in "${ROOMS[@]}"
        do 
            echo "Stopping RRFTracker: ${ROOM}"
            NOW=$(date +"%Y%m%d_%H%M%S")
            cp ${PATH_PID}/RRFTracker_${ROOM}.log ${PATH_PID}/RRFTracker_${ROOM}_${NOW}.log
            kill `cat ${PATH_PID}/RRFTracker_${ROOM}.pid`
        done
        ;;
esac