from networkx.algorithms import ancestors
import pandas as pd
import numpy as np
import networkx as nx
import utils.animals
from tqdm import tqdm

tqdm.pandas()

ALL_TAXON_RANKS = {"species": 0, "subgenus": 0.9, "genus": 1, "supergenus": 1.1, "infratribe": 1.3, "subtribe": 1.4, "tribe": 1.5, "supertribe": 1.6, "infrafamily": 1.8, "subfamily": 1.9, "family": 2, "epifamily": 2.05, "superfamily": 2.1, "subsection": 2.4, "section": 2.5, "parvorder": 2.7, "infraorder": 2.8, "suborder": 2.9,
                   "nanorder": 2.95, "order": 3, "superorder": 3.1, "parvclass": 3.7, "subterclass": 3.75, "infraclass": 3.8, "subclass": 3.9, "class": 4, "superclass": 4.1, "megaclass": 4.2, "gigaclass": 4.3, "parvphylum": 4.7, "infraphylum": 4.8, "subphylum": 4.9, "phylum": 5, "superphylum": 5.1, "subkingdom": 4.9, "kingdom": 5}


def distance_from_row(df, row1, row2):
    common = []
    sep1, sep2 = [], []
    first_common = ""
    d = -1

    anc1 = row1.ancestors.values[0]
    anc2 = row2.ancestors.values[0]
    for anc in anc1:
        row = df[df["taxonID"] == anc]
        name = row["genericName"].values[0]
        if name == "":
            name = row["scientificName"].values[0]
        if anc in anc2:  # if it is a common ancestor
            common.append(name)
            if first_common == "":
                first_common = anc
            if d < 0:
                rank = row["taxonRank"].values[0]
                d = ALL_TAXON_RANKS.get(rank, -1)
        else:  # if it is only an ancestor of 1
            sep1.append(name)
    for anc in anc2:
        if anc == first_common:  # keep only ancestors of 2
            break
        row = df[df["taxonID"] == anc]
        name = row["genericName"].values[0]
        if name == "":
            name = row["scientificName"].values[0]
        sep2.append(name)

    return d, sep1, sep2, common


def row_from_name(df, name):
    splitName = name.split(' ')
    for i in range(len(splitName), 0, -1):
        res = df[df["scientificName"].str.startswith(
            ' '.join(splitName[:i]))]
        if len(res) > 0:
            return res.head(1)
    return None


def distance(df, name1, name2):
    sciName1 = utils.animals.search(name1)
    sciName2 = utils.animals.search(name2)
    if sciName2 and sciName1:
        row1 = row_from_name(df, sciName1)
        row2 = row_from_name(df, sciName2)
        if len(row1) > 0 and len(row2) > 0:
            print("Computing distance between %s and %s" % (
                row1["scientificName"].values[0], row2["scientificName"].values[0]))

            return distance_from_row(df, row1, row2)
        return -1, "Not found"
    return -1, "Not found"


def get_roots(df):
    """
    to use if all roots are needed
    """
    return df.loc[df["taxonID"].str.len() == 1]["taxonID"]


def get_ancestors(df):
    # roots = get_roots(df)
    roots = ["N"]  # We only want animals in our case

    def ancestors(id):
        for tg in roots:
            try:
                a = list(nx.shortest_path(dg, source=tg, target=id))
                a.reverse()
                return a
            except nx.exception.NetworkXNoPath:
                pass
        return np.nan
    dg = nx.from_pandas_edgelist(
        df, source="parentNameUsageID", target="taxonID", create_using=nx.DiGraph)
    df["ancestors"] = df["taxonID"].map(ancestors)
    df.dropna(subset=['ancestors'], inplace=True)
    return df
