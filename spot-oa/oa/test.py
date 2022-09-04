from argparse import ArgumentParser

from components.geoloc.geoloc import GeoLocalization
import logging


def _parse_args():
    """
        Parse command-line options found in 'args' (default: sys.argv[1:]).

    :returns: On success, a namedtuple of Values instances.
    """
    parser = ArgumentParser('Check IP location', epilog='END')
    required = parser.add_argument_group('mandatory arguments')

    # .................................state optional arguments
    required.add_argument('-f', '--file',
                          help='IP location file',
                          metavar='')
    required.add_argument('-i', '--ip',
                          help='ip address',
                          metavar='')
    return parser.parse_args()


if __name__ == '__main__':
    logger = logging.getLogger('test')
    args = _parse_args()

    geo = GeoLocalization(args.file, logger)
    print geo.get_ip_geo_localization(args.ip)
