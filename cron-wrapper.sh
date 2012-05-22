#!/bin/bash

source /home/threebean/.bashrc
workon tw2-demos
python list-travis.py > index.html

if [ -d /home/threebean/webapps/tw2_tests ] ; then
    mv index.html  /home/threebean/webapps/tw2_tests/index.html
fi
