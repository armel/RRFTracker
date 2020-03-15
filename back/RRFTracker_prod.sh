#!/bin/sh

PATH_SCRIPT='/opt/RRFTracker_Web/back/RRFTracker.py'
PATH_MEDIA='/opt/RRFTracker_Web/front/assets'
PATH_HTML='/opt/RRFTracker_Web/front/index.html'

PATH_LOG='/var/www/RRFTracker'
PATH_PID='/tmp'

NOW=$(date +"%H%M%S")

case "$1" in
    start)
        cp -a $PATH_MEDIA $PATH_LOG
        echo "Starting RRFTracker: RRF"
        cp $PATH_HTML $PATH_LOG/RRF-today
        cp $PATH_LOG/RRF-today/rrf.json $PATH_LOG/RRF-today/rrf_$NOW.json
        nohup python $PATH_SCRIPT --room RRF --log-path $PATH_LOG > $PATH_PID/RRFTracker_RRF.log 2>&1 & echo $! > $PATH_PID/RRFTracker_RRF.pid
        echo "Starting RRFTracker: TECHNIQUE"
        cp $PATH_HTML $PATH_LOG/TECHNIQUE-today
        cp $PATH_LOG/TECHNIQUE-today/rrf.json $PATH_LOG/TECHNIQUE-today/rrf_$NOW.json
        nohup python $PATH_SCRIPT --room TECHNIQUE --log-path $PATH_LOG > $PATH_PID/RRFTracker_TECHNIQUE.log 2>&1 & echo $! > $PATH_PID/RRFTracker_TECHNIQUE.pid
        echo "Starting RRFTracker: BAVARDAGE"
        cp $PATH_HTML $PATH_LOG/BAVARDAGE-today
        cp $PATH_LOG/BAVARDAGE-today/rrf.json $PATH_LOG/BAVARDAGE-today/rrf_$NOW.json
        nohup python $PATH_SCRIPT --room BAVARDAGE --log-path $PATH_LOG > $PATH_PID/RRFTracker_BAVARDAGE.log 2>&1 & echo $! > $PATH_PID/RRFTracker_BAVARDAGE.pid
        echo "Starting RRFTracker: INTERNATIONAL"
        cp $PATH_HTML $PATH_LOG/INTERNATIONAL-today
        cp $PATH_LOG/INTERNATIONAL-today/rrf.json $PATH_LOG/INTERNATIONAL-today/rrf_$NOW.json
        nohup python $PATH_SCRIPT --room INTERNATIONAL --log-path $PATH_LOG > $PATH_PID/RRFTracker_INTERNATIONAL.log 2>&1 & echo $! > $PATH_PID/RRFTracker_INTERNATIONAL.pid
        echo "Starting RRFTracker: LOCAL"
        cp $PATH_HTML $PATH_LOG/LOCAL-today
        cp $PATH_LOG/LOCAL-today/rrf.json $PATH_LOG/LOCAL-today/rrf_$NOW.json
        nohup python $PATH_SCRIPT --room LOCAL --log-path $PATH_LOG > $PATH_PID/RRFTracker_LOCAL.log 2>&1 & echo $! > $PATH_PID/RRFTracker_LOCAL.pid
        #echo "Starting RRFTracker: EXPERIMENTAL"
        #cp $PATH_HTML $PATH_LOG/EXPERIMENTAL-today
        #nohup python $PATH_SCRIPT --room EXPERIMENTAL --log-path $PATH_LOG > $PATH_PID/RRFTracker_EXPERIMENTAL.log 2>&1 & echo $! > $PATH_PID/RRFTracker_EXPERIMENTAL.pid
        echo "Starting RRFTracker: FON"
        cp $PATH_HTML $PATH_LOG/FON-today
        cp $PATH_LOG/FON-today/rrf.json $PATH_LOG/FON-today/rrf_$NOW.json    
        nohup python $PATH_SCRIPT --room FON --log-path $PATH_LOG > $PATH_PID/RRFTracker_FON.log 2>&1 & echo $! > $PATH_PID/RRFTracker_FON.pid
        ;;
    stop) 
        echo "Stopping RRFTracker: RRF"
        kill `cat $PATH_PID/RRFTracker_RRF.pid`
        echo "Stopping RRFTracker: TECHNIQUE"
        kill `cat $PATH_PID/RRFTracker_TECHNIQUE.pid`
        echo "Stopping RRFTracker: BAVARDAGE"
        kill `cat $PATH_PID/RRFTracker_BAVARDAGE.pid`
        echo "Stopping RRFTracker: INTERNATIONAL"
        kill `cat $PATH_PID/RRFTracker_INTERNATIONAL.pid`
        echo "Stopping RRFTracker: LOCAL"
        kill `cat $PATH_PID/RRFTracker_LOCAL.pid`
        #echo "Stopping RRFTracker: EXPERIMENTAL"
        #kill `cat $PATH_PID/RRFTracker_EXPERIMENTAL.pid`
        echo "Stopping RRFTracker: FON"
        kill `cat $PATH_PID/RRFTracker_FON.pid`
        ;;
esac