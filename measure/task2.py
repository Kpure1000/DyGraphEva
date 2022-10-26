import networkx as nx
import numpy as np

from task_total import read_Graphs

def delta_sum(gs_metrics):
    keys_delta={}
    for key in gs_metrics[0]:
        delta_val=0
        for i in range(0, len(gs_metrics)-1):
            if i+1!=len(gs_metrics):
                delta_val += abs( gs_metrics[i+1][key] - gs_metrics[i][key] )
        keys_delta[key] = delta_val
    return keys_delta


def wipe_repeat(nodes, all_paris):
    paris_sp_s=set()
    paris_sp_l=[]
    for s in range(0,len(nodes)):
        for t in range(0, len(nodes)):
            pair_st = (nodes[s],nodes[t])
            if (s != t) and ( pair_st not in paris_sp_s and (nodes[t],nodes[s]) not in paris_sp_s ):
                paris_sp_s.add(pair_st)
                paris_sp_l.append({"id": pair_st, "val": all_paris[pair_st]})
    return paris_sp_l


def paired_shortest_paths(gs):
    gs_sp=[]
    for g in gs:
        g_sp={}
        nodes = list(g.nodes)
        for s in range(0,len(nodes)):
            for t in range(0, len(nodes)):
                if s != t:
                    try:
                        p_sp = 1/nx.shortest_path_length(G=g,source=nodes[s],target=nodes[t],weight="weight")
                    except: # networkx.exception.NetworkXNoPath
                        p_sp=0
                    pair = (nodes[s],nodes[t])
                    g_sp[pair]=p_sp
        gs_sp.append(g_sp)

    all_paris_sp = delta_sum(gs_sp)
    paris_sp_l = wipe_repeat(nodes=nodes, all_paris=all_paris_sp)
    paris_sp_l.sort(key=lambda ele: ele['val'], reverse=True)

    return paris_sp_l, gs_sp



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
        for s in range(0,len(nodes)):
            for t in range(0, len(nodes)): # 去重
                if s != t:
                    p_ki = S[s][t]
                    g_ki[(nodes[s], nodes[t])] = p_ki

        gs_ki.append(g_ki)

    all_pairs_ki = delta_sum(gs_ki)
    paris_ki_l = wipe_repeat(nodes=nodes, all_paris=all_pairs_ki)
    paris_ki_l.sort(key=lambda ele: ele['val'], reverse=True)

    return paris_ki_l, gs_ki



def paired_average_commute_time(gs):
    gs_mct=[]
    for g in gs:
        L = nx.laplacian_matrix(g).toarray()
        CTK = np.linalg.pinv(L)
        nodes = list(g.nodes)
        g_mct={}
        for s in range(0,len(nodes)):
            for t in range(0, len(nodes)): # 去重
                if s != t:
                    val = (CTK[s][s] + CTK[t][t] - 2 * CTK[s][t])
                    if val != 0:
                        p_mct = 1/(CTK[s][s] + CTK[t][t] - 2 * CTK[s][t])
                    else:
                        p_mct = 0
                    g_mct[(nodes[s],nodes[t])]=p_mct

        gs_mct.append(g_mct)

    all_paris_mct = delta_sum(gs_mct)
    paris_mct_l = wipe_repeat(nodes=nodes, all_paris=all_paris_mct)
    paris_mct_l.sort(key=lambda ele: ele['val'], reverse=True)

    return paris_mct_l, gs_mct


def paired_mean_commute_time(gs):
    gs_mct=[]
    for g in gs:
        L = nx.laplacian_matrix(g).toarray()
        CTK = np.linalg.pinv(L)
        nodes = list(g.nodes)
        g_mct={}
        for s in range(0,len(nodes)):
            for t in range(0, len(nodes)): # 去重
                if s != t:
                    p_mct = (CTK[s][s] + CTK[t][t] - 2 * CTK[s][t])
                    g_mct[(nodes[s],nodes[t])]=p_mct

        gs_mct.append(g_mct)

    all_paris_mct = delta_sum(gs_mct)
    paris_mct_l = wipe_repeat(nodes=nodes, all_paris=all_paris_mct)
    paris_mct_l.sort(key=lambda ele: ele['val'], reverse=True)

    return paris_mct_l, gs_mct

# gs = read_Graphs("../data/dataset/synth/test0/", "test")
# gs = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")
gs = read_Graphs("../data/dataset/synth/edge_eva/", "edge_eva")

# gs = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
# gs = read_Graphs("../data/dataset/truth/vdBunt_data/", "FR")


# nodes_mct, gs_mct = paired_shortest_paths(gs)
# print("[Shortest Paths] Variation (descend): ")
# for node_mct in nodes_mct:
#     print("Pair '{0}':\t{1:.7f}".format(node_mct['id'],node_mct['val']))

nodes_mct, gs_mct = paired_average_commute_time(gs)
print("[Average Commute Time] Variation (descend): ")
for node_mct in nodes_mct:
    print("Pair '{0}':\t{1:.7f}".format(node_mct['id'],node_mct['val']))

# nodes_mct, gs_mct = paired_mean_commute_time(gs)
# print("[Mean Commute Time] Variation (descend): ")
# for node_mct in nodes_mct:
#     print("Pair '{0}':\t{1:.7f}".format(node_mct['id'],node_mct['val']))

# nodes_ki, gs_ki = paired_katz_index(gs)
# print("[Katz Index] Variation (descend): ")
# for node_mct in nodes_ki:
#     print("Pair '{0}':\t{1:.7f}".format(node_mct['id'],node_mct['val']))
