from argparse import ArgumentParser
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
    required.add_argument('-d', '--db-file',
                          help='database file',
                          metavar='')

    required.add_argument('-q', '--query',
                          help='database file',
                          metavar='')

    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = _parse_args()
        query = args.query
        db_file = args.db_file

        conn = sl.connect(db_file)
        with conn:
            rows = conn.execute(query).fetchall()
            print rows

    except SystemExit:
        raise
    except:
        sys.excepthook(*sys.exc_info())
        sys, exit(1)
