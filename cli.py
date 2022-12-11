#!/usr/bin/env python3
import click
import utils.sql
import utils.tree
import os


@click.group()
def cli():
    pass


@cli.command(name="get_ancestors")
def get_ancestors():
    df = utils.sql.load()
    df = utils.tree.get_ancestors(df)
    df.to_json("species.json")


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
