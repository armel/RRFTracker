#!/bin/bash

PATH_SCRIPT='/opt/RRFTracker/back/RRFTracker.py'
PATH_MEDIA='/opt/RRFTracker/front/assets'
PATH_HTML='/opt/RRFTracker/front/index.html'
PATH_RRF='http://rrf.f5nlg.ovh:8080/RRFTracker'
PATH_LOG='/var/www/RRFTracker'
PATH_PID='/tmp'

NOW=$(date +"%H%M%S")

ROOMS=("RRF" "TECHNIQUE" "BAVARDAGE" "LOCAL" "INTERNATIONAL" "FON")

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
            mv ${PATH_PID}/RRFTracker_${ROOM}.log ${PATH_PID}/RRFTracker_${ROOM}_${NOW}.log
            kill `cat ${PATH_PID}/RRFTracker_${ROOM}.pid`
        done
        ;;
    reset)
        for ROOM in "${ROOMS[@]}"
        do
            cd ${PATH_LOG}/${ROOM}-today/
            curl -O ${PATH_RRF}/${ROOM}-today/rrf.json
        done
        ;;
    clear)
        for ROOM in "${ROOMS[@]}"
        do
            rm ${PATH_PID}/RRFTracker_${ROOM}_*.log
        done
        ;;
esac