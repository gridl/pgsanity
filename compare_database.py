# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import json
from optparse import OptionParser
from utils import create_database_session, collect_table_data
from termcolor import colored


def read_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def yay(text):
    print(colored(text, 'green'))


def nay(text):
    print(colored(text, 'red'))


def compare_values(msg, expected, actual, approved_diff=None):

    def close_enough(exp, act):
        if not approved_diff:
            return False

        expected_diff = approved_diff * min(exp, act)
        actual_diff = (abs(exp - act))
        return actual_diff < expected_diff

    if expected == actual or close_enough(expected, actual):
        yay('{0}: same: expected {1}, actual {2}.'.format(msg, expected, actual))
    else:
        nay('{0}: different: expected {1}, actual {2}.'.format(msg, expected, actual))


def compare_data(ref_data, table_data):
    compare_values('Number of tables', len(ref_data), len(table_data))

    for table_name in sorted(ref_data.keys()):
        if table_name in table_data:

            compare_values(
                '* {0} rows'.format(table_name),
                ref_data[table_name]['row_count'],
                table_data[table_name]['row_count'],
                approved_diff=0.1
            )

            for col_name in ref_data[table_name]['columns']:
                if col_name in table_data[table_name]['columns']:

                    if ref_data[table_name]['columns'][col_name]['primary_key']:

                        compare_values(
                            '  {0} min'.format(col_name),
                            ref_data[table_name]['columns'][col_name]['min_value'],
                            table_data[table_name]['columns'][col_name]['min_value'])

                        compare_values(
                            '  {0} max'.format(col_name),
                            ref_data[table_name]['columns'][col_name]['max_value'],
                            table_data[table_name]['columns'][col_name]['max_value'])
                else:
                    nay('  {0} field is missing.'.format(col_name))
        else:
            nay('* {0} table is missing.'.format(table_name))


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
        help='Input JSON filename (required).')
    (popts, pargs) = parser.parse_args()

    if not popts.database or not popts.filename:
        parser.print_help()
        exit(1)

    base, session = create_database_session(popts.database)
    reference_data = read_data(popts.filename)
    table_data = collect_table_data(base, session)
    compare_data(reference_data, table_data)
