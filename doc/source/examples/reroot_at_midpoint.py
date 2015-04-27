#! /usr/bin/env python

import dendropy

tree_str = "[&R] (A:0.55, (B:0.82, (C:0.74, (D:0.42, E:0.64):0.24):0.15):0.20):0.3;"

tree = dendropy.Tree.get(
        data=tree_str,
        schema="newick")

print("Before:")
print(tree.as_string(schema='newick'))
print(tree.as_ascii_plot(plot_metric='length'))
tree.reroot_at_midpoint(update_bipartitions=False)
print("After:")
print(tree.as_string(schema='newick'))
print(tree.as_ascii_plot(plot_metric='length'))

