#!/bin/bash
SERVERS=$1

spark-submit \
--driver-memory 24g \
--executor-memory 16g \
--packages "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.4,com.johnsnowlabs.nlp:spark-nlp_2.12:6.3.0" \
--files "log4j.properties" \
--conf "spark.driver.extraJavaOptions=-Dlog4j.configuration=file:log4j.properties" \
--conf "spark.executor.extraJavaOptions=-Dlog4j.configuration=file:log4j.properties" \
--conf "spark.serializer=org.apache.spark.serializer.KryoSerializer" \
--conf "spark.kryoserializer.buffer.max=2000M" \
./spark/model_test.py $SERVERS
