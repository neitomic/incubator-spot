#!/bin/bash

source /root/.bashrc
source /opt/impala/bin/impala-config.sh
cd /opt/incubator-spot/spot-ingest
source venv/bin/activate
echo $PATH

bash -c 'python start_listener.py -t flow --topic SPOT-INGEST-TEST-TOPIC-FLOW -p 1 --master yarn --deploy-mode client  --config-file ingest_conf.json --redirect-spark-logs logs/spark_streaming_spot_listener_flow.log'
