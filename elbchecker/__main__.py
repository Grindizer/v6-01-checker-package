import sys
from .runner import check_elb
from .connection import get_session, get_client
import optparse


def get_parser():
    parser = optparse.OptionParser(description='Smoke tests for aws elb', prog='checker', epilog='')
    parser.add_option('--regions', '-r', action='append', type='string', default=[], help='region list to run '
                                                                                          'the checks')
    return parser


def main(args=sys.argv):
    parser = get_parser()
    opts, args = parser.parse_args(args)
    for region in opts.regions:
        session = get_session({}, region)
        client = get_client('elb', session)
        for check_name, name, status in check_elb(client):
            print('{} :: {} :: {} -> {}'.format(region, name, check_name, status))


if __name__ == '__main__':
    sys.exit(main())
