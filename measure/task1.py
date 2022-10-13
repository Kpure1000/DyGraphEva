import networkx as nx
import numpy as np

from read_graph import read_Graphs
 
# 计算节点在每两个时间片的指标差值并求和
def delta_sum(node_indexs, gs_metrics):
    nodes_metrics = []
    for node_id in node_indexs:
        cc_delta = 0
        for i in range(0, gs_metrics.__len__() - 1):
            if i + 1 != gs_metrics.__len__():
                cc_delta += abs(gs_metrics[i + 1][node_id] - gs_metrics[i][node_id])
        nodes_metrics.append({'id': node_id, 'val': cc_delta})
    
    return nodes_metrics


def closeness_centrality(gs):
    ccs = []

    for g in gs:
        cc = nx.closeness_centrality(g, distance='weight')
        ccs.append(cc)

    nodes_cc = delta_sum(gs[0].nodes(), ccs)

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

    nodes_mct = delta_sum(gs[0].nodes(), gs_mct)

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

    nodes_mct = delta_sum(gs[0].nodes(), gs_mct)

    nodes_mct.sort(key=lambda ele: ele['val'], reverse=True)

    return nodes_mct

# gs = read_Graphs("../data/dataset/synth/test0/", "test")
gs = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
# gs = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")


nodes_cc = closeness_centrality(gs)
print("Node Closeness Centrality Variation (descend): ")
for node_cc in nodes_cc:
    print("Node '{0}':\t{1:.4f}".format(node_cc['id'],node_cc['val']))

# nodes_mct = average_commute_time(gs)
# print("Node Mean Commute Time Variation (descend): ")
# for node_mct in nodes_mct:
#     print("Node '{0}':\t{1:.4f}".format(node_mct['id'],node_mct['val']))
