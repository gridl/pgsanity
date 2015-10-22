# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime


DEBUG = False


def debug_message(*args):
    """
    Print out the message if DEBUG const is set
    :param args: list what to print
    """
    if DEBUG:
        print(*args)


def create_database_session(database_uri):
    """
    Connect to database and return base and session
    :param database_uri: string uri for psycopg2 to connect to db
    :return: tuple (base, session)
    """

    def name_for_scalar_relationship(bs, this, other, constr):
        name = other.__name__.lower() + '_ref'
        return name

    base = automap_base()
    engine = create_engine(database_uri)
    base.prepare(
        engine,
        reflect=True,
        name_for_scalar_relationship=name_for_scalar_relationship)
    session = Session(engine)
    return base, session


def collect_table_data(base, session):
    """
    Read table information from database and return dict:

    ```
    {
      "table_name_1": {
        "row_count": 100,
        "columns": {
          "col_name_1": {
            "type": "VARCHAR",
            "primary_key": true,
            "min_value": "aaa",
            "max_value": "zzz"
          }
        }
      },
      ...
    }
    ```

    :param base: base
    :param session: session
    :return: dict
    """

    all_tables = {}

    for table_class in base.classes:
        table_obj = table_class.__table__
        debug_message('--', table_obj.name)

        all_tables[table_obj.name] = {
            'row_count': session.query(table_obj).count(),
            'columns': {}
        }
        for table_col in table_obj.columns:
            col_dict = {
                'type': table_col.type.__visit_name__,
                'primary_key': table_col.primary_key,
            }
            if table_col.primary_key:
                minv = session.query(func.min(table_col)).first()[0]
                maxv = session.query(func.max(table_col)).first()[0]
                if isinstance(table_col.type, DateTime):
                    minv = str(minv)
                    maxv = str(maxv)

                col_dict['min_value'] = minv
                col_dict['max_value'] = maxv

            all_tables[table_obj.name]['columns'][table_col.name] = col_dict
            debug_message('  ', table_col.name, table_col.type)

    debug_message('Processed {0} tables.'.format(len(all_tables)))

    return all_tables
