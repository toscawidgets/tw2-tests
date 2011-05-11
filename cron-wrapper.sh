#!/bin/bash

source ~/.bashrc

pushd ~/tw2-tests
./generate-report.sh
pushd -
