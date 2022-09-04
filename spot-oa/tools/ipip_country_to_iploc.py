import re
from argparse import ArgumentParser
import sys

FILE_PATTERN = re.compile(r'ipip_country_(\w+).netset')
IP_PATTERN = re.compile(
    r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\/\d+)?$')


def _parse_args():
    """
        Parse command-line options found in 'args' (default: sys.argv[1:]).

    :returns: On success, a namedtuple of Values instances.
    """
    parser = ArgumentParser('Convert IPIP_location to iploc', epilog='END')
    required = parser.add_argument_group('mandatory arguments')

    # .................................state optional arguments
    required.add_argument('-s', '--src-dir',
                          help='source directory',
                          metavar='')
    required.add_argument('-d', '--dst-file',
                          help='destination file',
                          metavar='')
    return parser.parse_args()


def ip_to_int(ip_str):
    octets = ip_str.split('.')
    return int(octets[0]) * 16777216 + int(octets[1]) * 65536 + int(octets[2]) * 256 + int(octets[3])


if __name__ == '__main__':
    try:
        args = _parse_args()
        src_dir = args.src_dir
        dst_file = args.dst_file

        from os import listdir
        from os.path import isfile, join

        files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]
        from ipaddress import IPv4Network
        from data import countries

        with open(dst_file, 'w') as dst:

            for f in files:
                m = FILE_PATTERN.match(f)
                if not m:
                    print "Ignore file {} as it not match pattern".format(f)
                    continue
                country_code = m.group(1).upper()
                country_name = countries.get(country_code, 'unknown')
                print "Processing file {0} with country code: {1}".format(f, country_code)
                with open(join(src_dir, f)) as read:
                    lines = read.readlines()
                    for line in lines:
                        ip_match = IP_PATTERN.match(line.strip())
                        if ip_match:
                            net = IPv4Network(unicode(line.strip()))
                            ip_start = ip_to_int(str(net[0]))
                            ip_end = ip_to_int(str(net[net.num_addresses - 1]))
                            dst.write(','.join([str(ip_start), str(ip_end), country_code, country_name, '', '', '0', '0', 'unknown', 'unknown']))
                            dst.write("\n")

    except SystemExit:
        raise
    except:
        sys.excepthook(*sys.exc_info())
        sys, exit(1)
