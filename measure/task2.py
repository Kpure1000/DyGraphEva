import networkx as nx
import numpy as np

from task_total import read_Graphs

def delta_sum(gs_metrics):
    keys_delta=[]
    for key in gs_metrics[0]:
        delta_val=0
        for i in range(0, len(gs_metrics)-1):
            if i+1!=len(gs_metrics):
                delta_val += abs( gs_metrics[i+1][key] - gs_metrics[i][key] )
        keys_delta.append({"id":key,"val":delta_val})
    return keys_delta


def paired_shortest_paths(gs):
    gs_sp=[]
    for g in gs:
        g_sp={}
        nodes = list(g.nodes)
        for s in range(0,len(g)):
            for t in range(0, s): # 去重
                if(s != t):
                    try:
                        p_sp = 1/nx.shortest_path_length(G=g,source=nodes[s],target=nodes[t],weight="weight")
                    except: # networkx.exception.NetworkXNoPath 
                        p_sp=0
                    pair = (nodes[s],nodes[t])
                    g_sp[pair]=p_sp
        gs_sp.append(g_sp)
 
    paris_sp = delta_sum(gs_sp)

    paris_sp.sort(key=lambda ele: ele['val'], reverse=True)

    return paris_sp, gs_sp



def paired_katz_index(gs):
    gs_ki=[]
    for g in gs:
        A = nx.adjacency_matrix(g).toarray()
        I = np.identity(len(g))
        eigen_max = np.amax(np.double(nx.adjacency_spectrum(g)))
        Beta = 0.099999 * (1 / eigen_max) # Beta is a free parameter
        S = np.linalg.inv(I - Beta * A) - I

        nodes = list(g.nodes)
        g_ki={}
        for s in range(0,len(g)):
            for t in range(0, s): # 去重
                if(s != t):
                    p_ki = S[s][t]
                    g_ki[(nodes[s], nodes[t])] = p_ki

        gs_ki.append(g_ki)

    pairs_ki = delta_sum(gs_ki)

    pairs_ki.sort(key=lambda ele: ele['val'], reverse=True)

    return pairs_ki, gs_ki



def paired_average_commute_time(gs):
    gs_mct=[]
    for g in gs:
        L = nx.laplacian_matrix(g, nodelist=sorted(g.nodes)).toarray()
        CTK = np.linalg.pinv(L)
        g_mct={}
        nodes = list(g.nodes)
        for s in range(0,len(g)):
            for t in range(0, s): # 去重
                if(s != t):
                    p_mct = 1/(CTK[s][s] + CTK[t][t] - 2 * CTK[s][t])
                    pair = (nodes[s],nodes[t])
                    g_mct[pair]=p_mct

        gs_mct.append(g_mct)

    paris_mct = delta_sum(gs_mct)

    paris_mct.sort(key=lambda ele: ele['val'], reverse=True)

    return paris_mct, gs_mct


def paired_mean_commute_time(gs):
    gs_mct=[]
    for g in gs:
        L = nx.laplacian_matrix(g, nodelist=sorted(g.nodes)).toarray()
        CTK = np.linalg.pinv(L)
        g_mct={}
        nodes = list(g.nodes)
        for s in range(0,len(g)):
            for t in range(0, s): # 去重
                if(s != t):
                    p_mct = (CTK[s][s] + CTK[t][t] - 2 * CTK[s][t])
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
paired_shortest_paths

nodes_mct, gs_mct = paired_shortest_paths(gs)
print("[Shortest Paths] Variation (descend): ")
for node_mct in nodes_mct:
    print("Pair '{0}':\t{1:.7f}".format(node_mct['id'],node_mct['val']))

nodes_mct, gs_mct = paired_average_commute_time(gs)
print("[Average Commute Time] Variation (descend): ")
for node_mct in nodes_mct:
    print("Pair '{0}':\t{1:.7f}".format(node_mct['id'],node_mct['val']))

nodes_mct, gs_mct = paired_mean_commute_time(gs)
print("[Mean Commute Time] Variation (descend): ")
for node_mct in nodes_mct:
    print("Pair '{0}':\t{1:.7f}".format(node_mct['id'],node_mct['val']))


nodes_ki, gs_ki = paired_katz_index(gs)
print("[Katz Index] Variation (descend): ")
for node_mct in nodes_ki:
    print("Pair '{0}':\t{1:.7f}".format(node_mct['id'],node_mct['val']))

