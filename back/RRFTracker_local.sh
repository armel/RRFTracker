#!/bin/sh

PATH_SCRIPT='/Users/armel/Dropbox/RRFTracker_Web/back/RRFTracker.py'
PATH_MEDIA='/Users/armel/Dropbox/RRFTracker_Web/front/assets'
PATH_HTML='/Users/armel/Dropbox/RRFTracker_Web/front/index.html'
PATH_RRF='http://rrf.f5nlg.ovh:8080/RRFTracker/'

PATH_LOG='/Users/armel/Sites/RRF'
PATH_PID='/tmp'

CURRENT=$(pwd)

case "$1" in
    start)
        cp -a $PATH_MEDIA $PATH_LOG
        
        echo "Starting RRFTracker: RRF"
        cp $PATH_HTML $PATH_LOG/RRF-today
        cd $PATH_LOG/RRF-today/
        rm rrf.json
        curl -O $PATH_RRF/RRF-today/rrf.json
        cd $CURRENT
        nohup python $PATH_SCRIPT --room RRF --log-path $PATH_LOG > $PATH_PID/RRFTracker_RRF.log 2>&1 & echo $! > $PATH_PID/RRFTracker_RRF.pid
        
        echo "Starting RRFTracker: TECHNIQUE"
        cp $PATH_HTML $PATH_LOG/TECHNIQUE-today
        cd $PATH_LOG/TECHNIQUE-today/
        rm rrf.json
        curl -O $PATH_RRF/TECHNIQUE-today/rrf.json
        cd $CURRENT
        nohup python $PATH_SCRIPT --room TECHNIQUE --log-path $PATH_LOG > $PATH_PID/RRFTracker_TECHNIQUE.log 2>&1 & echo $! > $PATH_PID/RRFTracker_TECHNIQUE.pid
        
        echo "Starting RRFTracker: BAVARDAGE"
        cp $PATH_HTML $PATH_LOG/BAVARDAGE-today
        cd $PATH_LOG/BAVARDAGE-today/
        rm rrf.json
        curl -O $PATH_RRF/BAVARDAGE-today/rrf.json
        cd $CURRENT
        nohup python $PATH_SCRIPT --room BAVARDAGE --log-path $PATH_LOG > $PATH_PID/RRFTracker_BAVARDAGE.log 2>&1 & echo $! > $PATH_PID/RRFTracker_BAVARDAGE.pid
        
        echo "Starting RRFTracker: INTERNATIONAL"
        cp $PATH_HTML $PATH_LOG/INTERNATIONAL-today
        cd $PATH_LOG/INTERNATIONAL-today/
        rm rrf.json
        curl -O $PATH_RRF/INTERNATIONAL-today/rrf.json
        cd $CURRENT
        nohup python $PATH_SCRIPT --room INTERNATIONAL --log-path $PATH_LOG > $PATH_PID/RRFTracker_INTERNATIONAL.log 2>&1 & echo $! > $PATH_PID/RRFTracker_INTERNATIONAL.pid
        
        echo "Starting RRFTracker: LOCAL"
        cp $PATH_HTML $PATH_LOG/LOCAL-today
        cd $PATH_LOG/LOCAL-today/
        rm rrf.json
        curl -O $PATH_RRF/LOCAL-today/rrf.json
        cd $CURRENT
        nohup python $PATH_SCRIPT --room LOCAL --log-path $PATH_LOG > $PATH_PID/RRFTracker_LOCAL.log 2>&1 & echo $! > $PATH_PID/RRFTracker_LOCAL.pid
        
        echo "Starting RRFTracker: FON"
        cp $PATH_HTML $PATH_LOG/FON-today
        cd $PATH_LOG/FON-today/
        rm rrf.json
        curl -O $PATH_RRF/FON-today/rrf.json
        cd $CURRENT
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
        echo "Stopping RRFTracker: FON"
        kill `cat $PATH_PID/RRFTracker_FON.pid`
        ;;
esac