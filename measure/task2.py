import sys
import networkx as nx
import numpy as np

from task_total import read_Graphs
from task_total import print_l

import measurements as ms


def wipe_repeated_pair_list(nodes, all_paris):
    paris_sp_s=set()
    paris_sp_l=[]
    for s in range(0,len(nodes)):
        for t in range(0, len(nodes)):
            pair_st = (nodes[s],nodes[t])
            if (s != t) and ( pair_st not in paris_sp_s and (nodes[t],nodes[s]) not in paris_sp_s ):
                paris_sp_s.add(pair_st)
                paris_sp_l.append({"id": pair_st, "val": all_paris[pair_st]})
    return paris_sp_l


def all_pairs_delta(nodes, gs_metrics):
    all_paris_delta = ms.delta_sum(gs_metrics)

    paris_l = wipe_repeated_pair_list(nodes=nodes, all_paris=all_paris_delta)

    paris_l.sort(key=lambda ele: ele['val'], reverse=True)

    return paris_l


def t2_ShortestPath(Gs, print_lim=sys.maxsize):
    nodes = list(Gs[0].nodes)
    gs_measure = ms.all_pairs_measure([ms.ShortestPath(g) for g in Gs])
    pairs_delta_list = all_pairs_delta(nodes, gs_measure)

    print_l(pairs_delta_list, "Shortest Path", print_lim)


def t2_ACT(Gs, print_lim=sys.maxsize):
    nodes = list(Gs[0].nodes)
    gs_measure = ms.all_pairs_measure([ms.ACT(g) for g in Gs])
    pairs_delta_list = all_pairs_delta(nodes, gs_measure)
    print_l(pairs_delta_list, "ACT", print_lim)


def t2_MCT(Gs, print_lim=sys.maxsize):
    nodes = list(Gs[0].nodes)
    gs_measure = ms.all_pairs_measure([ms.MCT(g) for g in Gs])
    pairs_delta_list = all_pairs_delta(nodes, gs_measure)

    print_l(pairs_delta_list, "MCT", print_lim)


def t2_Katz(Gs, print_lim=sys.maxsize):
    nodes = list(Gs[0].nodes)
    gs_measure = ms.all_pairs_measure([ms.KatzIndex(g) for g in Gs])
    pairs_delta_list = all_pairs_delta(nodes, gs_measure)

    print_l(pairs_delta_list, "Katz", print_lim)


gs = read_Graphs("../data/dataset/synth/test0/", "test")
# gs = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")
# gs = read_Graphs("../data/dataset/synth/edge_eva/", "edge_eva")
# gs = read_Graphs("../data/dataset/synth/cluster/", "cluster")

# gs = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
# gs = read_Graphs("../data/dataset/truth/vdBunt_data/", "FR")


# t2_ShortestPath(gs, 10)
# t2_Katz(gs, 10)
# t2_MCT(gs, 10)
# t2_ACT(gs, 10)
