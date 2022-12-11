import pandas as pd
from os import environ as env


def _db_con():
    MYSQL_USER = env.get("MYSQL_USER", "ASI322")
    MYSQL_PASS = env.get("MYSQL_PASS", "")
    MYSQL_DB = env.get("MYSQL_DB", "ASI322")
    MYSQL_HOST = env.get("MYSQL_HOST", "localhost")

    MYSQL_URI = "mysql://%s:%s@%s/%s" % (MYSQL_USER, MYSQL_PASS,
                                         MYSQL_HOST, MYSQL_DB)
    return MYSQL_URI


def load(table="species_taxon"):
    """Load the table into a pandas dataframe
    The database connection parameters are obtained through env vars
        table: the name of the table to load
    """
    query = "SELECT * FROM %s where taxonomicStatus = 'ACCEPTED'" % table
    df = pd.read_sql(query, con=_db_con())
    return df


def dump(df, name="species"):
    """Dump the table to SQL
        name: The name of the target table
    """
    df.to_sql(name=name, con=_db_con())
