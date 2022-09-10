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

import logging
import sqlite3 as sl
from utils import Util


class Reputation(object):
    def __init__(self, conf, logger=None):
        self._firehol_database_file = conf['db_file']
        self._logger = logging.getLogger('OA.FIREHOL') if logger else Util.get_logger('OA.FIREHOL', create_file=False)
        # todo: load data set into db
        self._conn = sl.connect(self._firehol_database_file)

    def check(self, ips=None, urls=None, cat=False):
        self._logger.info("Threat-Exchange reputation check starts...")
        reputation_dict = {}
        data = []

        if ips is not None:
            values = ips
        elif urls is not None:
            self._logger.info("Firehol doesn't support URLs check.")
            return reputation_dict
        else:
            self._logger.info("Need either an ip or an url to check reputation.")
            return reputation_dict

        for val in values:

            if self._check_reputation("malicious", val):
                reputation_dict[val] = self._get_reputation_label("MALICIOUS")
            elif self._check_reputation("suspicious", val):
                reputation_dict[val] = self._get_reputation_label("SUSPICIOUS")
            else:
                reputation_dict[val] = self._get_reputation_label("UNKNOWN")

        return reputation_dict

    def _check_reputation(self, table, ip):
        with self._conn:
            ip_int = Util.ip_to_int(ip)
            cur = self._conn.execute("SELECT * FROM {} WHERE ip_start <= ? AND ip_end >= ?".format(table),
                                     (ip_int, ip_int))
            result = cur.fetchall()
            return len(result) > 0

    def _get_reputation_label(self, reputation):

        if reputation == 'UNKNOWN':
            return "firehol:UNKNOWN:-1"
        elif reputation == 'NON_MALICIOUS':
            return "firehol:NON_MALICIOUS:0"
        elif reputation == 'SUSPICIOUS':
            return "firehol:SUSPICIOUS:2"
        elif reputation == 'MALICIOUS':
            return "firehol:MALICIOUS:3"

