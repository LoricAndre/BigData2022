#!/usr/bin/env python3
import os
import pandas as pd
from pandarallel import pandarallel
import click
from os import environ as env

pandarallel.initialize(progress_bar=True)


@click.group()
def cli():
    pass


@cli.command(name="get_parents")
def get_parents():
    MYSQL_USER = env.get("MYSQL_USER", "ASI322")
    MYSQL_PASS = env.get("MYSQL_PASS", "")
    MYSQL_DB = env.get("MYSQL_DB", "ASI322")
    MYSQL_HOST = env.get("MYSQL_HOST", "localhost")

    MYSQL_URI = "mysql://%s:%s@%s/%s" % (MYSQL_USER, MYSQL_PASS,
                                         MYSQL_HOST, MYSQL_DB)
    query = "SELECT * FROM species_taxon where taxonomicStatus = 'accepted'"
    # Create a pandas dataframe
    df = pd.read_sql(query, con=MYSQL_URI)

    # Iterate over parents

    def get_parents(df, id):
        row = df[df["taxonID"].str.startswith(id)].head(1)
        parentId = ""
        for item in row["parentNameUsageID"]:
            parentId = item
            break
        if len(parentId) > 3:
            return [parentId] + get_parents(df, parentId)
        return []

    df["parents"] = df["taxonID"].parallel_map(lambda id: get_parents(df, id))

    df.to_sql("species", con=MYSQL_URI)
    click.echo("Computed parents and saved to table %s" % "species")


@cli.command(name="iter_filename")
@click.argument("path")
def iter_filename(path):
    fn, extension = os.path.splitext(path)
    i = 0
    while os.path.isfile(path):
        path = "%s%d%s" % (fn, i, extension)
        i += 1
    click.echo(path)


if __name__ == '__main__':
    cli()
