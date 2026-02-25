#!/bin/bash

SERVERS=$1
KAFKA_DIR="/opt/kafka"
KAFKA_CLUSTER_ID=$(${KAFKA_DIR}/bin/kafka-storage.sh random-uuid)
CONTROLLERS=""

for ((i=1; i<=SERVERS; i++)); do
	PORT=$((9090 + (i * 2) + 1))
	ENTRY="$i@localhost:$PORT"
	
	if [ -z "$CONTROLLERS" ]; then
		CONTROLLERS="$ENTRY"
	else
		CONTROLLERS="$CONTROLLERS,$ENTRY"
	fi
done

rm -rf /opt/kafka/logs/server-*-logs

for ((i=1; i<=SERVERS; i++)); do
	B_PORT=$((9090 + (i * 2)))
	C_PORT=$((B_PORT + 1))

	cp ${KAFKA_DIR}/config/server.properties ${KAFKA_DIR}/config/server-${i}.properties
	sed -i "s/^node.id=.*/node.id=${i}/" ${KAFKA_DIR}/config/server-${i}.properties
	sed -i "s|^listeners=.*|listeners=PLAINTEXT://localhost:${B_PORT},CONTROLLER://localhost:${C_PORT}|" ${KAFKA_DIR}/config/server-${i}.properties
	sed -i "s|^advertised.listeners=.*|advertised.listeners=PLAINTEXT://localhost:${B_PORT}|" ${KAFKA_DIR}/config/server-${i}.properties
	sed -i "s|^log.dirs=.*|log.dirs=/opt/kafka/logs/server-${i}-logs|" ${KAFKA_DIR}/config/server-${i}.properties
	echo controller.quorum.voters=$CONTROLLERS >> ${KAFKA_DIR}/config/server-${i}.properties
	echo "Server ${i} file generated."
done

for ((i=1; i<=SERVERS; i++)); do
	${KAFKA_DIR}/bin/kafka-storage.sh format -t ${KAFKA_CLUSTER_ID} -c ${KAFKA_DIR}/config/server-${i}.properties 
done

for ((i=1; i<=SERVERS; i++)); do
	${KAFKA_DIR}/bin/kafka-server-start.sh -daemon ${KAFKA_DIR}/config/server-${i}.properties
done

echo "Checking server(s) status"
sleep 3

for ((i=1; i<=SERVERS; i++)); do
	PORT=$((9091 + (i * 2)))
	${KAFKA_DIR}/bin/kafka-metadata-quorum.sh --bootstrap-controller localhost:${PORT} describe --status
done