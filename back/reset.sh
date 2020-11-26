#!/bin/bash

PATH_LOG='/var/www/RRFTracker'
PATH_RRF='http://rrf.f5nlg.ovh:8080/RRFTracker'

ROOMS=("RRF" "TECHNIQUE" "BAVARDAGE" "LOCAL" "INTERNATIONAL" "EXPERIMENTAL" "FON")

for ROOM in "${ROOMS[@]}"
do
    cd $PATH_LOG/$ROOM-today/
    curl -O $PATH_RRF/$ROOM-today/rrf.json
done