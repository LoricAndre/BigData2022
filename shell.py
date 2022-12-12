#!/usr/bin/env python3
import utils.tree
import pandas as pd
import networkx as nx
from glob import glob
from cmd import Cmd


class MyPrompt(Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "(no data) |>"
        self.json_files = glob("*.json", root_dir="data", recursive=True)
        self.loaded = False

    def emptyline(self):
        pass

    def do_load(self, file):
        try:
            self.df = pd.read_json("data/%s" % file)
            self.prompt = "(data: %s) |>" % file
            self.loaded = True
        except Exception as e:
            print("Error: %s" % str(e))

    def do_distance(self, names):
        try:
            name1, name2 = names.split()
            d, g = utils.tree.distance(self.df, name1, name2)
            if d != -1:
                print("Distance: %.1f" % d)
                utils.tree.draw(g)
            else:
                print("Species not found or not related")
        except Exception as e:
            print("Error: %s" % str(e))

    def do_draw(self, _):
        try:
            if self.loaded:
                dg = nx.from_pandas_edgelist(
                    self.df, source="parentNameUsageID", target="taxonID", create_using=nx.DiGraph)
                utils.tree.draw(dg, "scientificName")
        except Exception as e:
            print("Error: %s" % str(e))

    def complete_load(self, text, line, begidx, endidx):
        res = [s for s in self.json_files if s.startswith(text)]
        return res

    def help_load(self):
        print("Load JSON file.")

    def help_distance(self):
        print("Compute distance between two species with their names given as args")

    def help_draw(self):
        print("Draw current data as tree.")

    def default(self, cmd):
        try:
            self.mem = eval(cmd)
            print(self.mem)
        except Exception as e:
            print("Error: %s" % str(e))

    def do_exit(self, _):
        print("Goodbye !")
        return True
    do_EOF = do_exit


if __name__ == '__main__':
    MyPrompt().cmdloop()
