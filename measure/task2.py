import networkx as nx
import numpy as np

from read_graph import read_Graphs

def delta_sum(gs_ps_metrics):
    ps_metrics=[]
    for g0_pair in gs_ps_metrics[0]:
        for g_ps_metrics in gs_ps_metrics:
            print()
    return ps_metrics

def paired_mean_commute_time(gs):
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
                    g_mct[(nodes[s],nodes[t])]=s_mct

        gs_mct.append(g_mct)

    paris_mct = delta_sum(gs_mct)

    # paris_mct.sort(key=lambda ele: ele['val'], reverse=True)

    return paris_mct

# gs = read_Graphs("../data/dataset/synth/test0/", "test")
# gs = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
# gs = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")
gs = read_Graphs("../data/dataset/synth/edge_eva/", "edge_eva")


nodes_mct = paired_mean_commute_time(gs)
print("Node Pair Mean Commute Time Variation (descend): ")
for node_mct in nodes_mct:
    print("Node Pair '{0}':\t{1:.4f}".format(node_mct['id'],node_mct['val']))
