#!/bin/bash
SERVERS=$1

cd /home/a/
source vvv/bin/activate
python3 ./producer_test.py $SERVERS

