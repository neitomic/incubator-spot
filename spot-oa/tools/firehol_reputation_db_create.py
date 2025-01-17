from argparse import ArgumentParser

from ipaddress import IPv4Network
from utils import IP_PATTERN, ip_to_int
from os.path import isfile, join
import sqlite3 as sl
import sys


def _parse_args():
    """
        Parse command-line options found in 'args' (default: sys.argv[1:]).

    :returns: On success, a namedtuple of Values instances.
    """
    parser = ArgumentParser('Create Firehol reputation database', epilog='END')
    required = parser.add_argument_group('mandatory arguments')

    # .................................state optional arguments
    required.add_argument('-s', '--firehol-dir',
                          help='Firehol directory',
                          metavar='')
    required.add_argument('-d', '--db-file',
                          help='database file',
                          metavar='')
    return parser.parse_args()


def load_firehol_data_into_db(connection, table, firehol_file):
    insert_query = "INSERT OR IGNORE INTO {} (ip_start, ip_end) values(?, ?)".format(table)
    count = 0
    with open(firehol_file) as read:
        lines = read.readlines()
        for line in lines:
            ip_match = IP_PATTERN.match(line.strip())
            if ip_match:
                net = IPv4Network(unicode(line.strip()))
                ip_start = ip_to_int(str(net[0]))
                ip_end = ip_to_int(str(net[net.num_addresses - 1]))
                connection.execute(insert_query, (ip_start, ip_end))
                count += 1

    return count


if __name__ == '__main__':
    try:
        args = _parse_args()
        firehol_dir = args.firehol_dir
        db_file = args.db_file

        malicious_datasets = ["firehol_level1.netset", "firehol_level2.netset", "firehol_level3.netset"]
        suspicious_datasets = ["firehol_level4.netset"]

        conn = sl.connect(db_file)
        with conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS suspicious(ip_start INTEGER, ip_end INTEGER, PRIMARY KEY (ip_start, ip_end));")
            conn.execute("DELETE FROM suspicious;")

            conn.execute(
                "CREATE TABLE IF NOT EXISTS malicious( ip_start INTEGER, ip_end INTEGER, PRIMARY KEY (ip_start, ip_end));")
            conn.execute("DELETE FROM malicious;")

            for malicious_dataset in malicious_datasets:
                f = join(firehol_dir, malicious_dataset)
                if isfile(f):
                    print "Loading malicious_dataset into malicious table"
                    subnet_count = load_firehol_data_into_db(conn, "malicious", f)
                    print "Done with {} subnets".format(subnet_count)

            for suspicious_dataset in suspicious_datasets:
                f = join(firehol_dir, suspicious_dataset)
                if isfile(f):
                    print "Loading suspicious_dataset into suspicious table"
                    subnet_count = load_firehol_data_into_db(conn, "suspicious", f)
                    print "Done with {} subnets".format(subnet_count)


    except SystemExit:
        raise
    except:
        sys.excepthook(*sys.exc_info())
        sys, exit(1)
