import networkx as nx
from measurements import IMeasure, ShortestPath, ACT, MCT, KatzIndex, RWR
from task_total import read_Graphs, weight2length, print_l


def get_clusters(g, group='group'):
    clusters = {}
    for n in g.nodes:
        cl = g.nodes[n][group]
        if cl != None:
            if cl not in clusters:
                clusters[cl] = [n]
            else:
                clusters[cl].append(n)
    return clusters


def task4(gs, measures):
    '''
    intra-cluster
    '''
    gs_clusters = {g: get_clusters(g, 'group') for g in gs}
    gs_ms_cls = {}
    for g in gs_clusters:
        ms_cls = {}
        gs_ms_cls[g] = ms_cls
        cl_list = list(gs_clusters[g])
        for c1 in range(len(cl_list)):
            for c2 in range(len(cl_list)):
                if c1 != c2:
                    cl_1 = cl_list[c1]
                    cl_2 = cl_list[c2]
                    ms_cls[(cl_1, cl_2)] = 0.0
                    ms_cls[(cl_2, cl_1)] = 0.0
                    c1_nodes = gs_clusters[g][cl_1]
                    c2_nodes = gs_clusters[g][cl_2]
                    for u in range(len(c1_nodes)):
                        for v in range(len(c2_nodes)):
                            node_index_u = list(g.nodes).index(c1_nodes[u])
                            node_index_v = list(g.nodes).index(c2_nodes[v])
                            ms_cls[(cl_1, cl_2)] += measures[g].get(node_index_u, node_index_v)
                            ms_cls[(cl_2, cl_1)] = ms_cls[(cl_1, cl_2)]
                    ms_cls[(cl_1, cl_2)] /= float(len(c1_nodes) * len(c2_nodes))
                    ms_cls[(cl_2, cl_1)] = ms_cls[(cl_1, cl_2)]
        # print(ms_cls)

    cls = [cl for cl in gs_ms_cls[list(gs_ms_cls)[0]]] 

    cl_ms = {}
    for cl in cls:
        cl_ms[cl] = 0
        for i, g in enumerate(gs_ms_cls):
            if i < len(gs_ms_cls) - 1:
                left = gs_ms_cls[list(gs_ms_cls)[i+1]][cl]
                right = gs_ms_cls[list(gs_ms_cls)[i]][cl]
                cl_ms[cl] += abs(left - right)
    return cl_ms


gs = read_Graphs('../data/dataset/synth/cluster/', 'cluster')
# gs = read_Graphs('../data/dataset/synth/intra_cluster/', 'intra_cluster')
# gs = read_Graphs('../data/dataset/truth/primary/', 'primary')

gs = weight2length(gs)

cl_ms = task4(gs, {g: ShortestPath(g, 'length') for g in gs})
print(f'ShortestPath res: {cl_ms}')
print(f'max: {max(cl_ms, key=lambda el : cl_ms[el])}')

cl_ms = task4(gs, {g: MCT(g, 'weight') for g in gs})
print(f'MCT res: {cl_ms}')
print(f'max: {max(cl_ms, key=lambda el : cl_ms[el])}')
