import logging
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext(appName="test")
ssc = StreamingContext(sc, batchDuration=5)
from pyspark.streaming.kafka import KafkaUtils

zkQuorum = "Ubuntu-1804-bionic-64-minimal:2181"
groupId = "test"
topics = {
    "SPOT-INGEST-TEST-TOPIC-FLOW": 1
}
dstream = KafkaUtils.createStream(ssc, zkQuorum, groupId, topics,
                                  keyDecoder=lambda x: x, valueDecoder=lambda x: x)

dstream.foreachRDD(lambda x: logging.getLogger().info(x.count()))
