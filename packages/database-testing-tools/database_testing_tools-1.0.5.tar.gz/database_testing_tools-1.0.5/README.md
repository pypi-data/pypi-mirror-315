# database-testing-tools

Database Testing Tools comprises a suite of generalised tests to run on your database, and produce reports for a notebook. It is designed for pre-production checks for curated databases, but can also be useful for monitoring changes over time. It can be particularly useful when combined with [papermill](https://papermill.readthedocs.io/en/latest/), which can be used to parameterize, execute and store notebooks as part of your pipeline.

## Installation

```bash
pip install database_testing_tools
```

## Usage

The package implements a `Tester` class, from which you can invoke a number of built-in tests and optional plotting features.

```python
from database_testing_tools import Tester
test = Tester()
database = "my_database_name"
out = test.check_all_tables_return_data(db_name=database)
```

Tests return two outputs: the result of the test; and some nice graphical representation of the test - either a markdown table, or a plot using the [Altair](https://altair-viz.github.io/index.html) plotting library.

The class also collects the results of the tests for an overall report, which you can access with the `Tester.get_results_table()` function.

You can find [a notebook](https://github.com/moj-analytical-services/database-testing-tools/blob/main/tests/functions_demo_template.ipynb) which demonstrates the functions available in the package.

### Curated database assumptions - SCD2 vs Snapshotting

The tests in this package assume the database being tested is versioned in one of two ways:
1. [Slowly Changing Dimensions type 2 (SCD2)](https://en.wikipedia.org/wiki/Slowly_changing_dimension#Type_2:_add_new_row): where the database includes records of inserts and updates to records. In curated databases a start time and end time will be added to each record. The start time is when the record is either created or last updated; the end time is either when the record was next updated, or a date arbitrarily far in the future to signify that it is the current version of the record. By filtering on these dates, it is possible to view the state of the database at a given point in time.
2. Snapshots: when SCD2 isn't possible or is impractical, versions of the database are recorded with an associated snapshot date based on date of extraction.

These methods require different methods to compare versions of the database over time, so there are some separate functions to handle them in their own way.
### Query engines

By default, the package uses [pydbtools](https://github.com/moj-analytical-services/pydbtools) to run the queries in the package on a given Amazon Athena database. However, it is possible to connect to your own database by making an extension of the BaseQueryEngine class defined in [utils.py](https://github.com/moj-analytical-services/database-testing-tools/blob/main/database_testing_tools/utils.py).

An engine for [DuckDB](https://duckdb.org) is included, and is used for the demo and unit tests in this package. A basic use of the DuckDB engine looks like this:

```python
import duckdb
from database_testing_tools.utils import DuckDbEngine
from database_testing_tools import Tester

conn = duckdb.connect()
query_engine = DuckDbEngine(conn)
tester = Tester(query_engine=query_engine)
database = "some_database"

tester.check_all_tables_return_data(db_name=database)
```

Alternative database engines should follow a similar pattern to the DuckDB engine - an initialiser that includes the database connection object, and an implementation of the `run_query` function that runs a given SQL query and returns the result as a pandas dataframe. As the built-in tests use [the Trino SQL dialect](https://trino.io/docs/current/), it is recommended to transpile the SQL with [sqlglot](https://sqlglot.com/sqlglot.html) to ensure the tests are executed correctly.