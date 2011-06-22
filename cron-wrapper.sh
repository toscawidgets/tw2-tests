#!/bin/bash

source /home/threebean/.bashrc

LOG=/home/threebean/tw2-tests/nightly.log
pushd /home/threebean/tw2-tests
echo "************************"  > $LOG
echo "Starting up at   $(date)" >> $LOG
echo $(pwd) >> $LOG
/bin/bash generate-report.sh >> $LOG 2>&1
echo "Finishing up at  $(date)" >> $LOG
echo "************************" >> $LOG
pushd -
