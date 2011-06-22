#!/bin/bash

source ~/.bashrc

pushd ~/tw2-tests
./generate-report.sh > ~/tw2-tests/nightly.log 2>&1
pushd -
