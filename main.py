#!/usr/bin/env python3
import pandas as pd
import graph
import utils.dwca

# df = pd.read_json("species.json")
df = utils.dwca.load("data/backbone.zip")
print(df.columns)
# species = df[df["taxonRank"] == "species"]
# graph.by_type(species)
