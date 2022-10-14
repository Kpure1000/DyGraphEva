import networkx as nx
import numpy as np

from task_total import read_Graphs, delta_sum
 
def closeness_centrality(gs):
    ccs = []

    for g in gs:
        cc = nx.closeness_centrality(g, distance='weight')
        ccs.append(cc)

    nodes_cc = delta_sum(ccs)

    nodes_cc.sort(key=lambda ele: ele['val'], reverse=True)

    return nodes_cc


def mean_commute_time(gs):
    gs_mct=[]
    for g in gs:
        L = nx.laplacian_matrix(g, nodelist=sorted(g.nodes)).toarray()
        CTK = np.linalg.pinv(L)
        g_mct={}
        nodes = list(g.nodes)
        for s in range(0,nodes.__len__()):
            s_mct=0
            for t in range(0,nodes.__len__()):
                if(s != t):
                    s_mct += (CTK[s][s] + CTK[t][t] - 2 * CTK[s][t])
            g_mct[nodes[s]]=s_mct
        gs_mct.append(g_mct)

    nodes_mct = delta_sum(gs_mct)

    nodes_mct.sort(key=lambda ele: ele['val'], reverse=True)

    return nodes_mct


def average_commute_time(gs):
    gs_mct=[]
    for g in gs:
        L = nx.laplacian_matrix(g, nodelist=sorted(g.nodes)).toarray()
        CTK = np.linalg.pinv(L)
        g_mct={}
        nodes = list(g.nodes)
        for s in range(0,g.nodes.__len__()):
            s_mct=0
            for t in range(0,g.nodes.__len__()):
                if(s != t):
                    s_mct += 1/(CTK[s][s] + CTK[t][t] - 2 * CTK[s][t])
            g_mct[nodes[s]]=s_mct
        gs_mct.append(g_mct)

    nodes_mct = delta_sum(gs_mct)

    nodes_mct.sort(key=lambda ele: ele['val'], reverse=True)

    return nodes_mct

gs = read_Graphs("../data/dataset/synth/test0/", "test")
# gs = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
# gs = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")


nodes_cc = closeness_centrality(gs)
print("Node [Closeness Centrality] Variation (descend): ")
for node_cc in nodes_cc:
    print("Node '{0}':\t{1:.4f}".format(node_cc['id'],node_cc['val']))

nodes_act = average_commute_time(gs)
print("Node [Average Commute Time] Variation (descend): ")
for node_act in nodes_act:
    print("Node '{0}':\t{1:.4f}".format(node_act['id'],node_act['val']))

nodes_mct = mean_commute_time(gs)
print("Node [Mean Commute Time] Variation (descend): ")
for node_mct in nodes_mct:
    print("Node '{0}':\t{1:.4f}".format(node_mct['id'],node_mct['val']))
