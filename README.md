# ASI322 - Analysis of species

## Dependencies

This project requires MySQL and python with pip, as well as graphviz for graph drawing.
Python dependencies can be installed through `make install`

## Data

The data is from [the catalog of life](https://www.catalogueoflife.org/), specifically from [this export](https://api.checklistbank.org/dataset/9845/export.zip?format=DwCA).

It has been converted to SQL using [this tool](https://github.com/Canadensys/dwca2sql). The SQL file should then be saved as `data/species.sql`.

The data has then been slightly altered to make accesses and computations more efficient by adding a column using `make get_parents`. It is then saved to json as `data/animals.json`

## Setup

You need to create a MySQL user and a database that it can access.
Configuration is then done through environment variables :

- `MYSQL_DB` (defaults to ASI322)
- `MYSQL_USER` (defaults to ASI322)
- `MYSQL_PASS` (defaults to empty)
- `MYSQL_HOST` (defaults to localhost)
- `DB_FILE` (defaults to `data/species.sql`)

## Initialization

Simply run `make load`. This will load the file specified by `DB_FILE`.

Then, `make get_ancestors` will build the json file needed by the shell.

## Usage
Simply run `./shell.py` to access the interactive shell. An help is available by running `help`.

Two main commands are then available :
- `load <file>` will load a json file from the `data` directory
- `distance <name1> <name2>` will compute the distance between the two species and draw the corresponding subtree. It is currently set to search species from their name in french. This behavior might be changed by changing the default parameter in `utils.tree.search` or passing `en` as second argument.
