import networkx as nx
import numpy as np

from task_total import read_Graphs, delta_sum

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
                    g_mct[pair]=p_mct

        gs_mct.append(g_mct)

    paris_mct = delta_sum(gs_mct)

    paris_mct.sort(key=lambda ele: ele['val'], reverse=True)

    return paris_mct, gs_mct

# gs = read_Graphs("../data/dataset/synth/test0/", "test")
# gs = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
# gs = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")
gs = read_Graphs("../data/dataset/synth/edge_eva/", "edge_eva")


nodes_mct, gs_mct = paired_average_commute_time(gs)
print("Node Pairs [Average Commute Time] Variation (descend, fisrt 10 pairs): ")
i=0
for node_mct in nodes_mct:
    print("Pair '{0}':\t{1:.7f}".format(node_mct['id'],node_mct['val']))
    if i > 10:
        break
    # i+=1
