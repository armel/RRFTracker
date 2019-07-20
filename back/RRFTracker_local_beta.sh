#!/bin/sh

PATH_SCRIPT='/Users/armel/Dropbox/RRFTracker_Web/back/RRFTracker.py'
PATH_LOG='/Users/armel/Sites/RRF'
PATH_PID='/tmp'

case "$1" in
    start)
        echo "Starting RRFTracker: RRF"
        nohup python $PATH_SCRIPT --room RRF --log-path $PATH_LOG > $PATH_PID/RRFTracker_RRF.log 2>&1 & echo $! > $PATH_PID/RRFTracker_RRF.pid
        echo "Starting RRFTracker: RRF3"
        nohup python $PATH_SCRIPT --room RRF3 --log-path $PATH_LOG > $PATH_PID/RRFTracker_RRF3.log 2>&1 & echo $! > $PATH_PID/RRFTracker_RRF3.pid
        echo "Starting RRFTracker: TECHNIQUE"
        nohup python $PATH_SCRIPT --room TECHNIQUE --log-path $PATH_LOG > $PATH_PID/RRFTracker_TECHNIQUE.log 2>&1 & echo $! > $PATH_PID/RRFTracker_TECHNIQUE.pid
        echo "Starting RRFTracker: INTERNATIONAL"
        nohup python $PATH_SCRIPT --room INTERNATIONAL --log-path $PATH_LOG > $PATH_PID/RRFTracker_INTERNATIONAL.log 2>&1 & echo $! > $PATH_PID/RRFTracker_INTERNATIONAL.pid
        echo "Starting RRFTracker: FON"
        nohup python $PATH_SCRIPT --room FON --log-path $PATH_LOG > $PATH_PID/RRFTracker_FON.log 2>&1 & echo $! > $PATH_PID/RRFTracker_FON.pid
        ;;
    stop) 
        echo "Stopping RRFTracker: RRF"
        kill `cat $PATH_PID/RRFTracker_RRF.pid`
        echo "Stopping RRFTracker: RRF3"
        kill `cat $PATH_PID/RRFTracker_RRF3.pid`
        echo "Stopping RRFTracker: TECHNIQUE"
        kill `cat $PATH_PID/RRFTracker_TECHNIQUE.pid`
        echo "Stopping RRFTracker: INTERNATIONAL"
        kill `cat $PATH_PID/RRFTracker_INTERNATIONAL.pid`
        echo "Stopping RRFTracker: FON"
        kill `cat $PATH_PID/RRFTracker_FON.pid`
        ;;
    esac