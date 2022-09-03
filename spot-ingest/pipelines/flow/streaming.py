#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

'''
    Methods to be used during the streaming process.
'''

import datetime
import logging
from nfdump_schema import spot_nfdump_fields, nfdump_fields


def show(x):
    print(x)
    return x


class StreamPipeline:
    '''
        Create an input stream that pulls netflow messages from Kafka.

    :param ssc         : :class:`pyspark.streaming.context.StreamingContext` object.
    :param zkQuorum    : Zookeeper quorum (host[:port],...).
    :param groupId     : The group id for this consumer.
    :param topics      : Dictionary of topic -> numOfPartitions to consume. Each
                         partition is consumed in its own thread.
    '''

    def __init__(self, ssc, zkQuorum, groupId, topics):
        from common.serializer import deserialize
        from pyspark.streaming.kafka import KafkaUtils

        self.__dstream = KafkaUtils.createStream(ssc, zkQuorum, groupId, topics,
                                                 keyDecoder=lambda x: x, valueDecoder=deserialize)

    @property
    def dstream(self):
        '''
            Return the schema of this :class:`DataFrame` as a
        :class:`pyspark.sql.types.StructType`.
        '''
        return self.__dstream \
            .map(lambda x: show(x)) \
            .map(lambda x: x[1]) \
            .flatMap(lambda x: x) \
            .map(lambda x: x.split(','))

    @property
    def schema(self):
        '''
            Return the data type that represents a row from the received data list.
        '''
        from pyspark.sql.types import (FloatType, IntegerType, LongType,
                                       ShortType, StringType, StructField, StructType)

        return StructType(
            [
                StructField('treceived', StringType(), True),
                StructField('unix_tstamp', LongType(), True),
                StructField('tryear', IntegerType(), True),
                StructField('trmonth', IntegerType(), True),
                StructField('trday', IntegerType(), True),
                StructField('trhour', IntegerType(), True),
                StructField('trminute', IntegerType(), True),
                StructField('trsecond', IntegerType(), True),
                StructField('tdur', FloatType(), True),
                StructField('sip', StringType(), True),
                StructField('dip', StringType(), True),
                StructField('sport', IntegerType(), True),
                StructField('dport', IntegerType(), True),
                StructField('proto', StringType(), True),
                StructField('flag', StringType(), True),
                StructField('fwd', IntegerType(), True),
                StructField('stos', IntegerType(), True),
                StructField('ipkt', LongType(), True),
                StructField('ibyt', LongType(), True),
                StructField('opkt', LongType(), True),
                StructField('obyt', LongType(), True),
                StructField('input', IntegerType(), True),
                StructField('output', IntegerType(), True),
                StructField('sas', IntegerType(), True),
                StructField('das', IntegerType(), True),
                StructField('dtos', IntegerType(), True),
                StructField('dir', IntegerType(), True),
                StructField('rip', StringType(), True),
                StructField('y', ShortType(), True),
                StructField('m', ShortType(), True),
                StructField('d', ShortType(), True),
                StructField('h', ShortType(), True)
            ]
        )

    @property
    def segtype(self):
        '''
            Return the type of the received segments.
        '''
        return 'netflow segments'

    @staticmethod
    def parse(fields):
        '''
            Parsing and normalization of data in preparation for import.

        :param fields: Column fields of a row.
        :returns     : A list of typecast-ed fields, according to the table's schema.
        :rtype       : ``list``
        '''

        print ("parsing message: {0}".format(fields))
        date = datetime.datetime.strptime(fields[0], '%Y-%m-%d %H:%M:%S')
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
        second = date.second

        unix_tstamp = date.strftime('%s')

        if len(fields) > 30:
            field_index = nfdump_fields
        else:
            field_index = spot_nfdump_fields

        return [
            fields[0],
            long(unix_tstamp),
            year,
            month,
            day,
            hour,
            minute,
            second,
            float(fields[field_index['td']]),
            fields[field_index['sa']],
            fields[field_index['da']],
            int(fields[field_index['sp']]),
            int(fields[field_index['dp']]),
            fields[field_index['pr']],
            fields[field_index['flg']],
            int(fields[field_index['fwd']]),
            int(fields[field_index['stos']]),
            long(fields[field_index['ipkt']]),
            long(fields[field_index['ibyt']]),
            long(fields[field_index['opkt']]),
            long(fields[field_index['obyt']]),
            int(fields[field_index['in']]),
            int(fields[field_index['out']]),
            int(fields[field_index['sas']]),
            int(fields[field_index['das']]),
            int(fields[field_index['dtos']]),
            int(fields[field_index['dir']]),
            fields[field_index['ra']],
            int(year),
            int(month),
            int(day),
            int(hour),
        ]
