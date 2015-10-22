# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import json
from optparse import OptionParser
from utils import create_database_session, collect_table_data


def output_data(data, filename):
    if filename:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    else:
        print(json.dumps(table_data, indent=4))


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option(
        '-d',
        '--database',
        dest='database',
        help='Database URL for SQLAlchemy (required).')
    parser.add_option(
        '-f',
        '--filename',
        dest='filename',
        help='Output JSON filename. If not provided, output is printed to '
             'console.')
    (popts, pargs) = parser.parse_args()

    if not popts.database:
        parser.print_help()
        exit(1)

    base, session = create_database_session(popts.database)
    table_data = collect_table_data(base, session)
    output_data(table_data, popts.filename)
