#!/bin/bash -e
export IMPALA_HOME=/opt/impala
export KAFKA_HOME=/opt/kafka
export SPARK_HOME=/opt/spark
export PATH="$PATH:$KAFKA_HOME/bin:$SPARK_HOME/bin:/usr/sbin"

# activating environment
source /opt/impala/bin/impala-config.sh
source /opt/incubator-spot/spot-ingest/venv/bin/activate

SPOT_HOME=/opt/incubator-spot

echo "Update firehol IP sets"
update-ipsets

echo "Update local db"
SPOT_OA_HOME=$SPOT_HOME/spot-oa
python SPOT_OA_HOME/tools/firehol_reputation_db_create.py --firehol-dir /etc/firehol/ipsets --db-file SPOT_OA_HOME/context/firehol_reputation.db


