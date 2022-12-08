# ASI322 - Analysis of species

## Dependencies

This project requires MySQL and python with pip.

## Data

The data is from [the catalog of life](https://www.catalogueoflife.org/),
specifically from [this export](https://api.checklistbank.org/dataset/9845/export.zip?format=DwCA).
It has been converted to SQL using [this tool](https://github.com/Canadensys/dwca2sql).

The data has then been slightly altered to make accesses and computations more
efficient by adding a column using `utils.py get_parents`.

## Setup

You need to create a MySQL user and a database that it can access.
Configuration is then done through environment variables :

- `MYSQL_DB` (defaults to ASI322)
- `MYSQL_USER` (defaults to ASI322)
- `MYSQL_PASS` (defaults to empty)
- `MYSQL_HOST` (defaults to localhost)
- `DB_FILE` (defaults to `species.sql`)

## Initialization

Simply run `make load`. This will load the file specified by `DB_FILE`.

## Saving

Run `make save` to save the database to a file, specified by `DB_FILE`.
If the file exists, a number is appended before the extension.
