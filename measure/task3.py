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


def task3(gs, measures):
    '''
    intra-cluster
    '''
    gs_clusters = {g: get_clusters(g, 'group') for g in gs}
    gs_ms_cls = {}
    for g in gs_clusters:
        ms_cls = {}
        gs_ms_cls[g] = ms_cls
        for cl in gs_clusters[g]:
            cl_nodes = gs_clusters[g][cl]
            ms_cls[cl] = 0
            for u in range(len(cl_nodes)):
                for v in range(u):
                    node_index_u = list(g.nodes).index(cl_nodes[u])
                    node_index_v = list(g.nodes).index(cl_nodes[v])
                    ms_cls[cl] += measures[g].get(node_index_u, node_index_v)
            C = len(cl_nodes)
            ms_cls[cl] /= C * (C - 1.0) / 2.0
        print(ms_cls)
    
    

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


# gs = read_Graphs('../data/dataset/synth/cluster/', 'cluster')
gs = read_Graphs('../data/dataset/synth/intra_cluster/', 'intra_cluster')
# gs = read_Graphs('../data/dataset/truth/primary/', 'primary')

gs = weight2length(gs)

cl_ms = task3(gs, {g: ShortestPath(g, 'length') for g in gs})
print(f'ShortestPath res: {cl_ms}')
print(f'max: {max(cl_ms, key=lambda el : cl_ms[el])}')

# cl_ms = task3(gs, {g: ACT(g, 'weight') for g in gs})
# print(f'ACT res: {cl_ms}')
# print(f'max: {max(cl_ms, key=lambda el : cl_ms[el])}')

cl_ms = task3(gs, {g: MCT(g, 'weight') for g in gs})
print(f'MCT res: {cl_ms}')
print(f'max: {max(cl_ms, key=lambda el : cl_ms[el])}')
