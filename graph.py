#!/usr/bin/env python3
import matplotlib.pyplot as plt
from tqdm import tqdm

tqdm.pandas()


def by_type(df):
    def get_root(ancestors):
        print(ancestors)
        for a in ancestors[::-1]:
            if a != '':
                return a
    anc = df["ancestors"].progress_map(get_root)
    anc = anc.groupby(anc).count()
    print(anc)
    anc.plot.pie(subplots=True)
    plt.show()
