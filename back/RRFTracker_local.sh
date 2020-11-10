#!/bin/sh

PATH_SCRIPT='/Users/armel/Dropbox/RRFTracker/back/RRFTracker.py'
PATH_MEDIA='/Users/armel/Dropbox/RRFTracker/front/assets'
PATH_HTML='/Users/armel/Dropbox/RRFTracker/front/index.html'
PATH_RRF='http://rrf.f5nlg.ovh:8080/RRFTracker/'

PATH_LOG='/Users/armel/Sites/RRFTracker'
PATH_PID='/tmp'

CURRENT=$(pwd)
NOW=$(date +"%H%M%S")
REP=$(date +"%Y_%m_%d")

case "$1" in
    start)
        cp -a $PATH_MEDIA $PATH_LOG
        
        echo "Starting RRFTracker: RRF"
        if [ -d $PATH_LOG/RRF_$REP ] 
        then
            rm -rf $PATH_LOG/RRF_$REP
            rm $PATH_LOG/RRF-today
        fi
        mkdir $PATH_LOG/RRF_$REP
        ln -s $PATH_LOG/RRF_$REP $PATH_LOG/RRF-today
        cp $PATH_HTML $PATH_LOG/RRF-today
        cd $PATH_LOG/RRF-today/
        curl -O $PATH_RRF/RRF-today/rrf.json
        cd $CURRENT
        nohup python3 $PATH_SCRIPT --room RRF --log-path $PATH_LOG > $PATH_PID/RRFTracker_RRF.log 2>&1 & echo $! > $PATH_PID/RRFTracker_RRF.pid
        
        echo "Starting RRFTracker: TECHNIQUE"
        if [ -d $PATH_LOG/TECHNIQUE_$REP ] 
        then
            rm -rf $PATH_LOG/TECHNIQUE_$REP
            rm $PATH_LOG/TECHNIQUE-today
        fi
        mkdir $PATH_LOG/TECHNIQUE_$REP
        ln -s $PATH_LOG/TECHNIQUE_$REP $PATH_LOG/TECHNIQUE-today
        cp $PATH_HTML $PATH_LOG/TECHNIQUE-today
        cd $PATH_LOG/TECHNIQUE-today/
        curl -O $PATH_RRF/TECHNIQUE-today/rrf.json
        cd $CURRENT
        nohup python3 $PATH_SCRIPT --room TECHNIQUE --log-path $PATH_LOG > $PATH_PID/RRFTracker_TECHNIQUE.log 2>&1 & echo $! > $PATH_PID/RRFTracker_TECHNIQUE.pid
        
        echo "Starting RRFTracker: BAVARDAGE"
        if [ -d $PATH_LOG/BAVARDAGE_$REP ] 
        then
            rm -rf $PATH_LOG/BAVARDAGE_$REP
            rm $PATH_LOG/BAVARDAGE-today
        fi
        mkdir $PATH_LOG/BAVARDAGE_$REP
        ln -s $PATH_LOG/BAVARDAGE_$REP $PATH_LOG/BAVARDAGE-today
        cp $PATH_HTML $PATH_LOG/BAVARDAGE-today
        cd $PATH_LOG/BAVARDAGE-today/
        curl -O $PATH_RRF/BAVARDAGE-today/rrf.json
        cd $CURRENT
        nohup python3 $PATH_SCRIPT --room BAVARDAGE --log-path $PATH_LOG > $PATH_PID/RRFTracker_BAVARDAGE.log 2>&1 & echo $! > $PATH_PID/RRFTracker_BAVARDAGE.pid
        
        echo "Starting RRFTracker: INTERNATIONAL"
        if [ -d $PATH_LOG/INTERNATIONAL_$REP ] 
        then
            rm -rf $PATH_LOG/INTERNATIONAL_$REP
            rm $PATH_LOG/INTERNATIONAL-today
        fi
        mkdir $PATH_LOG/INTERNATIONAL_$REP
        ln -s $PATH_LOG/INTERNATIONAL_$REP $PATH_LOG/INTERNATIONAL-today
        cp $PATH_HTML $PATH_LOG/INTERNATIONAL-today
        cd $PATH_LOG/INTERNATIONAL-today/
        curl -O $PATH_RRF/INTERNATIONAL-today/rrf.json
        cd $CURRENT
        nohup python3 $PATH_SCRIPT --room INTERNATIONAL --log-path $PATH_LOG > $PATH_PID/RRFTracker_INTERNATIONAL.log 2>&1 & echo $! > $PATH_PID/RRFTracker_INTERNATIONAL.pid
        
        echo "Starting RRFTracker: LOCAL"
        if [ -d $PATH_LOG/LOCAL_$REP ] 
        then
            rm -rf $PATH_LOG/LOCAL_$REP
            rm $PATH_LOG/LOCAL-today
        fi
        mkdir $PATH_LOG/LOCAL_$REP
        ln -s $PATH_LOG/LOCAL_$REP $PATH_LOG/LOCAL-today
        cp $PATH_HTML $PATH_LOG/LOCAL-today
        cd $PATH_LOG/LOCAL-today/
        curl -O $PATH_RRF/LOCAL-today/rrf.json
        cd $CURRENT
        nohup python3 $PATH_SCRIPT --room LOCAL --log-path $PATH_LOG > $PATH_PID/RRFTracker_LOCAL.log 2>&1 & echo $! > $PATH_PID/RRFTracker_LOCAL.pid
        
        #echo "Starting RRFTracker: EXPERIMENTAL"
        #if [ -d $PATH_LOG/EXPERIMENTAL_$REP ] 
        #then
        #    rm -rf $PATH_LOG/EXPERIMENTAL_$REP
        #    rm $PATH_LOG/EXPERIMENTAL-today
        #fi
        #mkdir $PATH_LOG/EXPERIMENTAL_$REP
        #ln -s $PATH_LOG/EXPERIMENTAL_$REP $PATH_LOG/EXPERIMENTAL-today
        #cp $PATH_HTML $PATH_LOG/EXPERIMENTAL-today
        #cd $PATH_LOG/EXPERIMENTAL-today/
        #curl -O $PATH_RRF/EXPERIMENTAL-today/rrf.json
        #cd $CURRENT
        #nohup python3 $PATH_SCRIPT --room EXPERIMENTAL --log-path $PATH_LOG > $PATH_PID/RRFTracker_EXPERIMENTAL.log 2>&1 & echo $! > $PATH_PID/RRFTracker_EXPERIMENTAL.pid
        
        echo "Starting RRFTracker: FON"
        if [ -d $PATH_LOG/FON_$REP ] 
        then
            rm -rf $PATH_LOG/FON_$REP
            rm $PATH_LOG/FON-today
        fi
        mkdir $PATH_LOG/FON_$REP
        ln -s $PATH_LOG/FON_$REP $PATH_LOG/FON-today
        cp $PATH_HTML $PATH_LOG/FON-today
        cd $PATH_LOG/FON-today/
        curl -O $PATH_RRF/FON-today/rrf.json
        cd $CURRENT
        nohup python3 $PATH_SCRIPT --room FON --log-path $PATH_LOG > $PATH_PID/RRFTracker_FON.log 2>&1 & echo $! > $PATH_PID/RRFTracker_FON.pid
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