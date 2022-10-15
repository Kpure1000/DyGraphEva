import networkx as nx
import numpy as np

from task_total import read_Graphs

def delta_sum(gs_metrics):
    keys_delta={}
    for key in gs_metrics[0]:
        delta_val=0
        for i in range(0, gs_metrics.__len__()-1):
            if i+1!=gs_metrics.__len__():
                delta_val += abs( gs_metrics[i+1][key] - gs_metrics[i][key] )
        keys_delta[key]=delta_val
    return keys_delta


def closeness_centrality(gs):
    ccs = []

    for g in gs:
        cc = nx.closeness_centrality(g, distance='weight')
        ccs.append(cc)

    nodes_cc_dict = delta_sum(ccs)

    nodes_cc=[]
    for node_cc in nodes_cc_dict:
        nodes_cc.append({"id": node_cc, "val": nodes_cc_dict[node_cc]})

    nodes_cc.sort(key=lambda ele: ele['val'], reverse=True)

    return nodes_cc


def shortest_paths(gs):
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
 
    pairs_sp = delta_sum(gs_sp)

    nodes_sp_dict={}
    nodes=list(gs[0].nodes)
    for s in range(0,len(nodes)):
        nodes_sp_dict[nodes[s]]=0
        for t in range(0,s):
            if(s != t):
                nodes_sp_dict[nodes[s]] += pairs_sp[(nodes[s], nodes[t])]
                nodes_sp_dict[nodes[t]] += pairs_sp[(nodes[s], nodes[t])]

    nodes_sp=[]
    for node_sp in nodes_sp_dict:
        nodes_sp.append({"id": node_sp, "val": nodes_sp_dict[node_sp]})

    nodes_sp.sort(key=lambda ele: ele['val'], reverse=True)

    return nodes_sp


def mean_commute_time(gs):
    gs_mct=[]
    for g in gs:
        L = nx.laplacian_matrix(g, nodelist=sorted(g.nodes)).toarray()
        CTK = np.linalg.pinv(L)
        g_mct={}
        nodes = list(g.nodes)
        for s in range(0,len(g)):
            for t in range(0,s):
                if(s != t):
                    s_mct = (CTK[s][s] + CTK[t][t] - 2 * CTK[s][t])
                    g_mct[(nodes[s],nodes[t])]=s_mct
        gs_mct.append(g_mct)

    pairs_mct = delta_sum(gs_mct)

    nodes_mct_dict={}
    nodes=list(gs[0].nodes)
    for s in range(0,len(nodes)):
        nodes_mct_dict[nodes[s]]=0
        for t in range(0,s):
            if(s != t):
                nodes_mct_dict[nodes[s]] += pairs_mct[(nodes[s], nodes[t])]
                nodes_mct_dict[nodes[t]] += pairs_mct[(nodes[s], nodes[t])]

    nodes_mct=[]
    for node_mct in nodes_mct_dict:
        nodes_mct.append({"id": node_mct, "val": nodes_mct_dict[node_mct]})

    nodes_mct.sort(key=lambda ele: ele['val'], reverse=True)

    return nodes_mct


def average_commute_time(gs):
    gs_mct=[]
    for g in gs:
        L = nx.laplacian_matrix(g, nodelist=sorted(g.nodes)).toarray()
        CTK = np.linalg.pinv(L)
        g_mct={}
        nodes = list(g.nodes)
        for s in range(0,len(g)):
            for t in range(0,s):
                if(s != t):
                    s_mct = 1/(CTK[s][s] + CTK[t][t] - 2 * CTK[s][t])
                    g_mct[(nodes[s],nodes[t])]=s_mct
        gs_mct.append(g_mct)

    pairs_mct = delta_sum(gs_mct)

    nodes_mct_dict={}
    nodes=list(gs[0].nodes)
    for s in range(0,len(nodes)):
        nodes_mct_dict[nodes[s]]=0
        for t in range(0,s):
            if(s != t):
                nodes_mct_dict[nodes[s]] += pairs_mct[(nodes[s], nodes[t])]
                nodes_mct_dict[nodes[t]] += pairs_mct[(nodes[s], nodes[t])]

    nodes_mct=[]
    for node_mct in nodes_mct_dict:
        nodes_mct.append({"id": node_mct, "val": nodes_mct_dict[node_mct]})

    nodes_mct.sort(key=lambda ele: ele['val'], reverse=True)

    return nodes_mct


def katz_index(gs):
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

    nodes_ki_dict={}
    nodes=list(gs[0].nodes)
    for s in range(0,len(nodes)):
        nodes_ki_dict[nodes[s]]=0
        for t in range(0,s):
            if(s != t):
                nodes_ki_dict[nodes[s]] += pairs_ki[(nodes[s], nodes[t])]
                nodes_ki_dict[nodes[t]] += pairs_ki[(nodes[s], nodes[t])]

    nodes_ki=[]
    for node_ki in nodes_ki_dict:
        nodes_ki.append({"id": node_ki, "val": nodes_ki_dict[node_ki]})

    nodes_ki.sort(key=lambda ele: ele['val'], reverse=True)

    return nodes_ki


# gs = read_Graphs("../data/dataset/synth/test0/", "test")
# gs = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
gs = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")


# nodes_cc = closeness_centrality(gs)
# print("[Closeness Centrality] Variation (descend): ")
# for node_cc in nodes_cc:
#     print("Node '{0}':\t{1:.4f}".format(node_cc['id'],node_cc['val']))

nodes_sp = shortest_paths(gs)
print("[Short Paths] Variation (descend): ")
for node_act in nodes_sp:
    print("Node '{0}':\t{1:.4f}".format(node_act['id'],node_act['val']))

nodes_act = average_commute_time(gs)
print("[Average Commute Time] Variation (descend): ")
for node_act in nodes_act:
    print("Node '{0}':\t{1:.4f}".format(node_act['id'],node_act['val']))

nodes_mct = mean_commute_time(gs)
print("[Mean Commute Time] Variation (descend): ")
for node_mct in nodes_mct:
    print("Node '{0}':\t{1:.4f}".format(node_mct['id'],node_mct['val']))

nodes_kz = katz_index(gs)
print("[Katz Index Time] Variation (descend): ")
for node_mct in nodes_kz:
    print("Node '{0}':\t{1:.4f}".format(node_mct['id'],node_mct['val']))
