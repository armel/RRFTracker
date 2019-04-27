#!/bin/sh

PATH_SCRIPT='/opt/RRFTracker_Web/back/RRFTracker.py'
PATH_LOG='/var/www/RRFTracker'
PATH_PID='/tmp'

case "$1" in
    start)
        echo "Starting RRFTracker: RRF"
        nohup python $PATH_SCRIPT --room RRF --log-path $PATH_LOG > $PATH_PID/RRFTracker_RRF.log 2>&1 & echo $! > $PATH_PID/RRFTracker_RRF.pid
        echo "Starting RRFTracker: TEC"
        nohup python $PATH_SCRIPT --room TEC --log-path $PATH_LOG > $PATH_PID/RRFTracker_TEC.log 2>&1 & echo $! > $PATH_PID/RRFTracker_TEC.pid
        ;;
    stop) 
        echo "Stopping RRFTracker: RRF"
        kill `cat $PATH_PID/RRFTracker_RRF.pid`
        echo "Stopping RRFTracker: TEC"
        kill `cat $PATH_PID/RRFTracker_TEC.pid`
        ;;
    esac