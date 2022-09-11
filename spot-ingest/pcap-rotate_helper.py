import re
from datetime import datetime, timedelta
from argparse import ArgumentParser
from common.file_watcher import FileWatcher
from common.utils import Util
from shutil import copyfile

import os
from os.path import basename, dirname
import logging
import sys


class PCAPRotateHelper:
    """
        Helper to delay file rotate.
    """

    def __init__(self, src_dir, dst_dir, windows_sec, supported_files, recursive=False):
        self._src_dir = src_dir
        self._dst_dir = dst_dir
        self._windows_sec = int(windows_sec)
        self._isalive = True
        self._supported_files = supported_files
        self._pattern = re.compile(r"([^_]+)_(\d+)_(\d+)\.pcap")

        self.FileWatcher = FileWatcher(src_dir, supported_files, recursive)
        self._logger = logging.getLogger('SPOT.INGEST.COMMON.FILE_ROTATE_HELPER')

    def start(self):
        self._logger.info('Start File Rotate Helper!')
        print 'Start File Rotate Helper from src {} to {}'.format(self._src_dir, self._dst_dir)
        if not os.path.exists(self._dst_dir):
            os.makedirs(self._dst_dir)

        self.FileWatcher.start()
        self._logger.info('Signal the {0} thread to start.'.format(str(self.FileWatcher)))
        print 'Signal the {0} thread to start.'.format(str(self.FileWatcher))

        try:
            while self._isalive:
                _file = self.FileWatcher.dequeue
                if _file:
                    self._logger.info("new file detected {}".format(_file))
                    print "new file dectected {}".format(_file)
                    filename = basename(_file)
                    previous_filename = self.find_previous_file(filename)

                    previous_file = os.path.join(dirname(_file), previous_filename)
                    print "previous file {}".format(previous_file)
                    if os.path.isfile(previous_file):
                        dst_file = os.path.join(self._dst_dir, previous_filename)
                        print "copy file {} -> {}".format(previous_file, dst_file)
                        copyfile(previous_file, dst_file)

                        print "trying to find older file to clean up"
                        to_delete_file_name = self.find_previous_file(previous_filename)
                        to_delete_file = os.path.join(dirname(_file), to_delete_file_name)
                        if os.path.isfile(to_delete_file):
                            print "deleting old file: {}".format(to_delete_file)
                            os.remove(to_delete_file)

                import time
                time.sleep(2)

        except KeyboardInterrupt:
            pass
        finally:
            self.FileWatcher.stop()
            self._logger.info('Stop File Rotate Helper!')

    def find_previous_file(self, filename):
        match = self._pattern.match(filename)
        if match:
            previous_counter = int(match.group(2)) - 1
            last_time = datetime.strptime(match.group(3), '%Y%m%d%H%M%S') - timedelta(seconds=self._windows_sec)
            if previous_counter >= 0:
                return "{}_{}_{}.pcap".format(match.group(1), str(previous_counter).zfill(5),
                                              last_time.strftime("%Y%m%d%H%M%S"))

        return None

    @classmethod
    def run(cls):
        try:
            args = _parse_args()

            # .........................set up logger
            Util.get_logger('ROTATE_HELPER', args.log_level)

            rotate_helper = cls(args.src_dir, args.dst_dir, args.windows_sec, [".pcap"])
            rotate_helper.start()

        except SystemExit:
            raise
        except:
            sys.excepthook(*sys.exc_info())
            sys, exit(1)


def _parse_args():
    '''
        Parse command-line options found in 'args' (default: sys.argv[1:]).

    :returns: On success, a namedtuple of Values instances.
    '''
    parser = ArgumentParser('Apache Spot PCAP file rotate helper', epilog='END')
    required = parser.add_argument_group('mandatory arguments')

    # .................................state optional arguments
    required.add_argument('-s', '--src-dir',
                          help='source directory',
                          metavar='')
    required.add_argument('-d', '--dst-dir',
                          help='destination directory',
                          metavar='')
    required.add_argument('-w', '--windows-sec',
                          help='rotate windows second',
                          metavar='')

    parser.add_argument('-l', '--log-level',
                        default='INFO',
                        help='determine the level of the logger',
                        metavar='')

    return parser.parse_args()


if __name__ == '__main__':
    PCAPRotateHelper.run()
