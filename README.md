Database sanity checks
======================

This is a utility script to check the data in PostgreSQL database assuming that
you have a "reference" database to compare to.

Workflow
--------

* Step 1: collect the data from your "reference" database.

```
$ python explore_database.py -d postgres://username:password@localhost/reference_dbname -f reference_dbname.json
```

The script will connect to the database specified by `-d` parameter and collect the information
such as table names, row counts, min and max values of primary key fields. This information 
will be written in JSON format into file specified by `-f` parameter.

* Step 2: collect the data from your actual database and compare with "reference".

```
$ python compare_database.py -d postgres://username:password@localhost/actual_dbname -f reference_dbname.json
```

The script will print out the comparison results. Example:

```
* table_1 rows: same: expected 100, actual 100.
  field_1 min: same: expected aaa, actual aaa.
  field_1 max: same: expected zzz, actual zzz.
* table_2 rows: different: expected 41002, actual 0.
  field_1 min: different: expected 00501, actual None.
  field_1 max: different: expected 99950, actual None.
```