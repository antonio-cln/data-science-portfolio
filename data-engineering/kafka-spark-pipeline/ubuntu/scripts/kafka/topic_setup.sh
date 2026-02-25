#!/bin/bash

SERVER_NUMBER=$1
SERVER_LIST=""
REPL=$2
PART=$3
KAFKA_DIR="/opt/kafka"

for ((i=1; i<=SERVER_NUMBER; i++)); do
	PORT=$((9090 + (i * 2)))
	ENTRY="localhost:$PORT"
	
	if [ -z "$SERVER_LIST" ]; then
		SERVER_LIST="$ENTRY"
	else
		SERVER_LIST="$SERVER_LIST,$ENTRY"
	fi
done

${KAFKA_DIR}/bin/kafka-topics.sh --create --topic tweet-train --bootstrap-server $SERVER_LIST --replication-factor $REPL --partitions $PART
${KAFKA_DIR}/bin/kafka-topics.sh --create --topic tweet-test --bootstrap-server $SERVER_LIST --replication-factor $REPL --partitions $PART
${KAFKA_DIR}/bin/kafka-topics.sh --describe --topic tweet-train --bootstrap-server $SERVER_LIST
${KAFKA_DIR}/bin/kafka-topics.sh --describe --topic tweet-test --bootstrap-server $SERVER_LIST