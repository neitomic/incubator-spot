#!/bin/bash -e

data_type=$1

export IMPALA_HOME=/opt/impala
export KAFKA_HOME=/opt/kafka
export SPARK_HOME=/opt/spark
export PATH="$PATH:$KAFKA_HOME/bin:$SPARK_HOME/bin"

# activating environment
source /opt/impala/bin/impala-config.sh
source /opt/incubator-spot/spot-ingest/venv/bin/activate

SPOT_HOME=/opt/incubator-spot

data_date=$(date -d "-10 min" "+%Y%m%d")
echo "Running operator for $data_type on $data_date"

cd $SPOT_HOME/spot-ml
./ml_ops.sh $data_date $data_type 0.5 200


cd $SPOT_HOME/spot-oa/oa
python start_oa.py -d $data_date -t $data_type -l 200
