import networkx as nx
from measurements import ShortestPath
from task_total import read_Graphs

def wipe_repeated_pair_list(nodes_l, all_pairs):
    '''
    Param
    -----
    nodes_l: list, nodes
    all_pairs: dict
    
    Return
    -----
    pairs_d: dict, no repeated pairs
    '''
    pairs_s=set()
    pairs_d={}
    for s in range(0,len(nodes_l)):
        for t in range(0, len(nodes_l)):
            pair_st = (nodes_l[s],nodes_l[t])
            if (s != t) and ( pair_st not in pairs_s and (nodes_l[t],nodes_l[s]) not in pairs_s ):
                pairs_s.add(pair_st)
                pairs_d[pair_st] = all_pairs[pair_st]
    return pairs_d


def nodes_cluster(G, group):
    cluster_nodes={}
    for i, node in enumerate(G):
        cur_group = G.nodes[node][group]
        if cur_group not in cluster_nodes:
            cluster_nodes[cur_group] = {}
        cluster_nodes[cur_group][node] = G.nodes[node]
    return cluster_nodes


def gs_pairs_in_cluster(gs, group='group', weight='weight'):
    clusters_pair={}
    for g in gs:
        g_node_list = list(g.nodes)
        cluster_nodes = nodes_cluster(g, group)
        cluster_pair={}
        measure = ShortestPath(g, weight)
        for cluster in cluster_nodes:
            cl_nodes_list = list(cluster_nodes[cluster])
            cluster_pair[cluster] = {}
            for s in cl_nodes_list:
                for t in cl_nodes_list:
                    cluster_pair[cluster][(s, t)] = \
                        measure.get(g_node_list.index(s), g_node_list.index(t))

            cluster_pair[cluster] = wipe_repeated_pair_list(
                list(cluster_nodes[cluster]), cluster_pair[cluster]
            )

        clusters_pair[g] = cluster_pair

    return clusters_pair


def simple_cluster():
    clusters = [20, 20, 20]
    links = [
        [0.7, 0.1, 0.2],
        [0.1, 0.7, 0.1],
        [0.2, 0.1, 0.7],
    ]
    G = nx.stochastic_block_model(clusters, links, seed=0)
    nx.set_edge_attributes(G, 1.0, 'weight')

    nx.draw_networkx(G)
    import matplotlib.pyplot as plt
    plt.show()

    G0=G.copy()
    G0.add_edge(0, 6, weight=1.0)
    G0.add_edge(6, 12, weight=1.0)


    return [G0]


# gs = read_Graphs('../data/dataset/synth/cluster/', 'cluster')
gs = read_Graphs('../data/dataset/synth/intra_cluster/', 'intra_cluster')

# gs = simple_cluster()

gs_clusters_pair = gs_pairs_in_cluster(gs=gs, group='group', weight='weight')


gs_ms=[]

for gi,g in enumerate(gs_clusters_pair):
    gs_ms_cl={}
    for cl in gs_clusters_pair[g]:
        gs_ms_cl[cl]=0
        for pair in gs_clusters_pair[g][cl]:
            gs_ms_cl[cl] += gs_clusters_pair[g][cl][pair]
        gs_ms_cl[cl] /= float(len(gs_clusters_pair[g][cl]))
    gs_ms.append(gs_ms_cl)

from measurements import delta_sum

print(delta_sum(gs_ms))
