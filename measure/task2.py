import networkx as nx
import numpy as np

from read_graph import read_Graphs

def delta_sum(gs_ps_metrics):
    ps_metrics=[]
    for g0_pair in gs_ps_metrics[0]:
        delta=0
        for i in range(0, gs_ps_metrics.__len__()-1):
            if i+1!=gs_ps_metrics.__len__():
                delta += abs( gs_ps_metrics[i+1][g0_pair] - gs_ps_metrics[i][g0_pair] )
        ps_metrics.append({"id":g0_pair,"val":delta})
    return ps_metrics

def paired_average_commute_time(gs):
    gs_mct=[]
    for g in gs:
        L = nx.laplacian_matrix(g, nodelist=sorted(g.nodes)).toarray()
        CTK = np.linalg.pinv(L)
        g_mct={}
        nodes = list(g.nodes)
        for s in range(0,nodes.__len__()):
            for t in range(0, s): # 去重
                if(s != t):
                    p_mct = 1/(CTK[s][s] + CTK[t][t] - 2 * CTK[s][t])
                    pair = (nodes[s],nodes[t])
                    print("pair{0}mct:{1}".format(pair,p_mct))
                    g_mct[pair]=p_mct

        gs_mct.append(g_mct)

    paris_mct = delta_sum(gs_mct)

    paris_mct.sort(key=lambda ele: ele['val'], reverse=True)

    return paris_mct

# gs = read_Graphs("../data/dataset/synth/test0/", "test")
# gs = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
gs = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")
# gs = read_Graphs("../data/dataset/synth/edge_eva/", "edge_eva")


nodes_mct = paired_average_commute_time(gs)
print("Node Pair Average Commute Time Variation (descend): ")
for node_mct in nodes_mct:
    print("Node Pair '{0}':\t{1:.8f}".format(node_mct['id'],node_mct['val']))

print(nodes_mct[0])