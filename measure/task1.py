import sys
import networkx as nx
import numpy as np

from task_total import read_Graphs, weight2length, print_l
import measurements as ms

def pairs2nodes(all_nodes, all_pairs):
    nodes_dict = {}
    for s in range(0, len(all_nodes)):
        nodes_dict[all_nodes[s]] = 0
        for t in range(0, len(all_nodes)):  # with repeat
            if(s != t):
                nodes_dict[all_nodes[s]] += all_pairs[(all_nodes[s], all_nodes[t])]

    return [{"id": node, "val": nodes_dict[node]} for node in nodes_dict]


def all_node_delta(nodes, gs_metrics):
    all_pairs_delta = ms.delta_sum(gs_metrics)
    nodes_l = pairs2nodes(all_nodes=list(gs[0].nodes), all_pairs=all_pairs_delta)
    nodes_l.sort(key=lambda ele: ele['val'], reverse=True)

    return nodes_l


def t1_ShortestPath(Gs, weight='weight', print_lim=sys.maxsize):
    nodes = list(Gs[0].nodes)
    gs_measure = ms.all_pairs_measure([ms.ShortestPath(g,weight) for g in Gs])
    nodes_delta_l = all_node_delta(nodes, gs_measure)

    print_l(nodes_delta_l, "Shortest Path", print_lim)


def t1_ACT(Gs, weight='weight', print_lim=sys.maxsize):
    nodes = list(Gs[0].nodes)
    gs_measure = ms.all_pairs_measure([ms.ACT(g,weight) for g in Gs])
    nodes_delta_l = all_node_delta(nodes, gs_measure)

    print_l(nodes_delta_l, "ACT", print_lim)


def t1_MCT(Gs, weight='weight', print_lim=sys.maxsize):
    nodes = list(Gs[0].nodes)
    gs_measure = ms.all_pairs_measure([ms.MCT(g,weight) for g in Gs])
    nodes_delta_l = all_node_delta(nodes, gs_measure)

    print_l(nodes_delta_l, "MCT", print_lim)


def t1_Katz(Gs, weight='weight', print_lim=sys.maxsize):
    nodes = list(Gs[0].nodes)
    gs_measure = ms.all_pairs_measure([ms.KatzIndex(g, weight,0.9) for g in Gs])
    nodes_delta_l = all_node_delta(nodes, gs_measure)

    print_l(nodes_delta_l, "Katz", print_lim)


# gs = read_Graphs("../data/dataset/synth/cluster/", "cluster")

# gs = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
# gs = read_Graphs("../data/dataset/truth/vdBunt_data/", "FR")
# gs = read_Graphs("../data/dataset/truth/vdBunt_data/", "VRND32T")
# gs = read_Graphs("../data/dataset/truth/mammalia-pa/", "mammalia-pa")

# gs = read_Graphs("../data/dataset/truth/canVote/", "canVote")
# gs = read_Graphs("../data/dataset/truth/reality_mining/", "reality_mining")
gs = read_Graphs("../data/dataset/truth/ambassador/", "ambassador")

gs = weight2length(gs)

t1_ShortestPath(gs,'length',5)
# t1_ACT(gs,'weight',5)
t1_MCT(gs,'weight',5)
t1_Katz(gs,'lenght',5)
