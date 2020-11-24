#!/bin/bash

PATH_SCRIPT='/Users/armel/Dropbox/RRFTracker/back/RRFTracker.py'
PATH_MEDIA='/Users/armel/Dropbox/RRFTracker/front/assets'
PATH_HTML='/Users/armel/Dropbox/RRFTracker/front/index.html'
PATH_RRF='http://rrf.f5nlg.ovh:8080/RRFTracker'

PATH_LOG='/Users/armel/Sites/RRFTracker'
PATH_PID='/tmp'

CURRENT=$(pwd)
NOW=$(date +"%H%M%S")
REP=$(date +"%Y-%m-%d")

ROOMS=("RRF" "TECHNIQUE" "BAVARDAGE" "LOCAL" "INTERNATIONAL" "EXPERIMENTAL" "FON")

case "$1" in
    start)
        for ROOM in "${ROOMS[@]}"
        do
            cp -a $PATH_MEDIA $PATH_LOG
            
            echo "Init RRFTracker: $ROOM"
            if [ -d ${PATH_LOG}/${ROOM}-${REP} ] 
            then
                rm -rf ${PATH_LOG}/${ROOM}-${REP}
                rm $PATH_LOG/$ROOM-today
            fi
            mkdir ${PATH_LOG}/${ROOM}-${REP}
            ln -s ${PATH_LOG}/${ROOM}-${REP} $PATH_LOG/$ROOM-today
            cp $PATH_HTML $PATH_LOG/$ROOM-today
            cd $PATH_LOG/$ROOM-today/
            curl -O $PATH_RRF/$ROOM-today/rrf.json
        done       
        echo "Starting RRFTracker"
        cd $CURRENT
        nohup python3 $PATH_SCRIPT --log-path $PATH_LOG > $PATH_PID/RRFTracker.log 2>&1 & echo $! > $PATH_PID/RRFTracker.pid
        ;;
    stop) 
        echo "Stopping RRFTracker"
        cp $PATH_PID/RRFTracker.log $PATH_PID/RRFTracker_${NOW)_${REP}.log
        kill `cat $PATH_PID/RRFTracker.pid`
        ;;
esac