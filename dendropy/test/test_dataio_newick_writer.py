
#! /usr/bin/env python

##############################################################################
##  DendroPy Phylogenetic Computing Library.
##
##  Copyright 2010 Jeet Sukumaran and Mark T. Holder.
##  All rights reserved.
##
##  See "LICENSE.txt" for terms and conditions of usage.
##
##  If you use this work or any portion thereof in published work,
##  please cite it as:
##
##     Sukumaran, J. and M. T. Holder. 2010. DendroPy: a Python library
##     for phylogenetic computing. Bioinformatics 26: 1569-1571.
##
##############################################################################

"""
Tests for NEWICK writing.
"""

import collections
import unittest
import dendropy
from dendropy.test.support import pathmap
from dendropy.test.support import datagen_standard_file_test_trees
from dendropy.test.support import compare_and_validate

class NewickTreeWriterTests(
        datagen_standard_file_test_trees.StandardTestTreeChecker,
        compare_and_validate.ValidateWriteable,
        unittest.TestCase):

    schema_tree_filepaths = dict(datagen_standard_file_test_trees.tree_filepaths["newick"])

    def get_simple_tree(self,
            has_leaf_node_taxa=False,
            has_leaf_node_labels=False,
            has_internal_node_taxa=False,
            has_internal_node_labels=False,
            has_edge_lengths=True,
            label_pool=None,
            label_separator=' ',
            ):
        anodes = set()
        tree = dendropy.Tree()
        tns = tree.taxon_namespace
        a = tree.seed_node.new_child()
        b = tree.seed_node.new_child()
        a1 = a.new_child()
        a2 = a.new_child()
        b1 = b.new_child()
        b2 = b.new_child()
        anodes.add(tree.seed_node)
        anodes.add(a)
        anodes.add(b)
        anodes.add(a1)
        anodes.add(a2)
        anodes.add(b1)
        anodes.add(b2)
        if label_pool is None:
            label_pool = [chr(i) for i in range(ord('a'), ord('z')+1)]
        labeller = iter(label_pool)
        for nd_idx, nd in enumerate(anodes):
            expected_label_parts = collections.defaultdict(list)
            is_leaf = nd.is_leaf()
            if ( (is_leaf and has_leaf_node_taxa)
                    or ((not is_leaf) and has_internal_node_taxa) ):
                label = next(labeller)
                tx = tree.taxon_namespace.require_taxon(label=label)
                nd.taxon = tx
                expected_label_parts[ (False, True ) ].append(label)
                expected_label_parts[ (False, False) ].append(label)
            if ( (is_leaf and has_leaf_node_labels)
                    or ((not is_leaf) and has_internal_node_labels) ):
                label = next(labeller)
                nd.label = label
                expected_label_parts[ (True,  False) ].append(label)
                expected_label_parts[ (False, False) ].append(label)
            nd.expected_label = collections.defaultdict(lambda: None)
            for k in expected_label_parts:
                nd.expected_label[k] = label_separator.join(expected_label_parts[k])
            if has_edge_lengths:
                nd.edge.length = nd_idx
        return tree

    def test_roundtrip_full(self):
        tree_file_title = 'standard-test-trees-n33-annotated'
        tree_filepath = datagen_standard_file_test_trees.tree_filepaths["newick"][tree_file_title]
        tree1 = dendropy.Tree.get_from_path(
                tree_filepath,
                "newick",
                extract_comment_metadata=True,
                store_tree_weights=True,
                suppress_internal_node_taxa=False,
                suppress_leaf_node_taxa=False,
        )
        kwargs = {
            "suppress_leaf_taxon_labels"     :  False , # default: False ,
            "suppress_leaf_node_labels"      :  True  , # default: True  ,
            "suppress_internal_taxon_labels" :  False , # default: False ,
            "suppress_internal_node_labels"  :  True  , # default: False ,
            "suppress_rooting"               :  False , # default: False ,
            "suppress_edge_lengths"          :  False , # default: False ,
            "unquoted_underscores"           :  False , # default: False ,
            "preserve_spaces"                :  False , # default: False ,
            "store_tree_weights"             :  False , # default: False ,
            "suppress_annotations"           :  False , # default: True  ,
            "annotations_as_nhx"             :  False , # default: False ,
            "suppress_item_comments"         :  False , # default: True  ,
            "node_label_element_separator"   :  ' '   , # default: ' '   ,
            "node_label_compose_func"        :  None  , # default: None  ,
            "edge_label_compose_func"        :  None  , # default: None  ,
        }
        s = self.write_out_validate_equal_and_return(
                tree1, "newick", kwargs)
        tree2 = dendropy.Tree.get_from_string(
                s,
                "newick",
                extract_comment_metadata=True,
                store_tree_weights=True,
                suppress_internal_node_taxa=False,
                suppress_leaf_node_taxa=False,
        )
        self.compare_to_check_tree(
            tree=tree2,
            tree_file_title=tree_file_title,
            check_tree_idx=0,
            suppress_internal_node_taxa=False,
            suppress_leaf_node_taxa=False,
            metadata_extracted=True,
            distinct_nodes_and_edges=False)

    def test_node_labeling(self):
        for has_leaf_node_taxa in (True, False):
            for has_leaf_node_labels in (True, False):
                for has_internal_node_taxa in (True, False):
                    for has_internal_node_labels in (True, False):
                        for label_separator in (' ', '$$$'):
                            tree = self.get_simple_tree(
                                    has_leaf_node_taxa=has_leaf_node_taxa,
                                    has_leaf_node_labels=has_leaf_node_labels,
                                    has_internal_node_taxa=has_internal_node_taxa,
                                    has_internal_node_labels=has_internal_node_labels,
                                    label_separator=label_separator,
                                    )
                            for suppress_leaf_taxon_labels in (True, False):
                                for suppress_leaf_node_labels in (True, False):
                                    for suppress_internal_taxon_labels in (True, False):
                                        for suppress_internal_node_labels in (True, False):
                                            kwargs = {
                                                    "suppress_leaf_taxon_labels"     : suppress_leaf_taxon_labels,
                                                    "suppress_leaf_node_labels"      : suppress_leaf_node_labels,
                                                    "suppress_internal_taxon_labels" : suppress_internal_taxon_labels,
                                                    "suppress_internal_node_labels"  : suppress_internal_node_labels,
                                                    "node_label_element_separator"   : label_separator,
                                                    }
                                            s = self.write_out_validate_equal_and_return(
                                                    tree, "newick", kwargs)
                                            tree2 = dendropy.Tree.get_from_string(
                                                    s,
                                                    "newick",
                                                    extract_comment_metadata=True,
                                                    store_tree_weights=True,
                                                    suppress_internal_node_taxa=True,
                                                    suppress_leaf_node_taxa=True,
                                            )
                                            nodes1 = [nd for nd in tree]
                                            nodes2 = [nd for nd in tree2]
                                            self.assertEqual(len(nodes1), len(nodes2))
                                            for nd1, nd2 in zip(nodes1, nodes2):
                                                is_leaf = nd1.is_leaf()
                                                self.assertEqual(nd2.is_leaf(), is_leaf)
                                                if is_leaf:
                                                    self.assertEqual(nd2.label,
                                                            nd1.expected_label[(suppress_leaf_taxon_labels, suppress_leaf_node_labels)])
                                                else:
                                                    self.assertEqual(nd2.label,
                                                            nd1.expected_label[ (suppress_internal_taxon_labels, suppress_internal_node_labels) ])
    def test_rooting_token(self):
        tree1 = self.get_simple_tree()
        for rooted_state in (None, True, False):
            tree1.is_rooted = rooted_state
            for suppress_rooting in (True, False):
                kwargs = {
                        "suppress_rooting": suppress_rooting,
                }
                s = self.write_out_validate_equal_and_return(
                        tree1, "newick", kwargs)
                if suppress_rooting:
                    self.assertFalse(s.startswith("[&R]") or s.startswith("[&U]"))
                else:
                    if rooted_state is True:
                        self.assertTrue(s.startswith("[&R]"))
                    elif rooted_state is False:
                        self.assertTrue(s.startswith("[&U]"))
                    else:
                        self.assertFalse(s.startswith("[&R]") or s.startswith("[&U]"))
                tree2 = dendropy.Tree.get_from_string(
                        s, "newick", rooting=None)
                if suppress_rooting:
                    self.assertTrue(tree2.is_rootedness_undefined)
                else:
                    if rooted_state is True:
                        self.assertTrue(tree2.is_rooted)
                        self.assertFalse(tree2.is_unrooted)
                    elif rooted_state is False:
                        self.assertFalse(tree2.is_rooted)
                        self.assertTrue(tree2.is_unrooted)
                    else:
                        self.assertTrue(tree2.is_rootedness_undefined)

    def test_edge_lengths(self):
        tree1 = self.get_simple_tree()
        for suppress_edge_lengths in (True, False):
            kwargs = {
                    "suppress_edge_lengths": suppress_edge_lengths,
            }
            s = self.write_out_validate_equal_and_return(
                    tree1, "newick", kwargs)
            tree2 = dendropy.Tree.get_from_string(
                    s, "newick", rooting=None)
            nodes1 = [nd for nd in tree1]
            nodes2 = [nd for nd in tree2]
            self.assertEqual(len(nodes1), len(nodes2))
            for nd1, nd2 in zip(nodes1, nodes2):
                if suppress_edge_lengths:
                    self.assertIs(nd2.edge.length, None)
                else:
                    self.assertEqual(nd2.edge.length, nd1.edge.length)

if __name__ == "__main__":
    unittest.main()