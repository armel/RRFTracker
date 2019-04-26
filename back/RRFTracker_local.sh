#!/bin/sh

PATH_SCRIPT='/Users/armel/Dropbox/RRFTracker_Web/back/RRFTracker.py'
PATH_LOG='/Users/armel/WebRoot/armel/RRF'
PATH_PID='/tmp'

case "$1" in
    start)
        echo "Starting RRFTracker: RRF"
        nohup python $PATH_SCRIPT --room RRF --log-path $PATH_LOG > /dev/null 2>&1 & echo $! > $PATH_PID/RRFTracker_RRF.pid
        echo "Starting RRFTracker: TEC"
        nohup python $PATH_SCRIPT --room TEC --log-path $PATH_LOG > /dev/null 2>&1 & echo $! > $PATH_PID/RRFTracker_TEC.pid
        ;;
    stop) 
        echo "Stopping RRFTracker: RRF"
        kill `cat $PATH_PID/RRFTracker_RRF.pid`
        echo "Stopping RRFTracker: TEC"
        kill `cat $PATH_PID/RRFTracker_TEC.pid`
        ;;
    esac