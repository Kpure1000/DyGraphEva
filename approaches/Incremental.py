from copy import deepcopy
import networkx as nx
import numpy as np
from FM3 import fm3_layout


def Merging(Gi, Gi_1, Li_1, dl):
    # find new nodes
    nodesi = set(Gi.nodes())        # nodes of Gi
    nodesi_1 = set(Gi_1.nodes())    # nodes of Gi-1
    ndoes_new = nodesi - nodesi_1
    nx.katz_centrality

    # bounding box of Li-1
    bounding_box = [np.array([float('inf'), float('inf')]), np.array([float('-inf'), float('-inf')])]
    for node in Li_1:
        bounding_box[0][0] = min(bounding_box[0][0], Li_1[node][0])
        bounding_box[0][1] = min(bounding_box[0][1], Li_1[node][1])
        bounding_box[1][0] = max(bounding_box[1][0], Li_1[node][0])
        bounding_box[1][1] = max(bounding_box[1][1], Li_1[node][1])

    # center of bounding box
    center_bx = 0.5 * ( bounding_box[0] + bounding_box[1] )
    bounding_box_size = bounding_box[1] - bounding_box[0]
    
    # neibs of all node in Gi
    neibs={}
    for node in nodesi:
        neibs[node] = list(nx.neighbors(G=Gi, n=node))

    contribution_factor_level = [0.0, 0.1, 0.25, 1.0]
    contribution_factor={}
    Li = Li_1.copy()
    for node in ndoes_new:
        neibs_new = set(neibs[node]) & ndoes_new # neibs i
        neibsi_1 = set(neibs[node]) & nodesi_1 # neibs i-1
        neibslen = len(neibsi_1)
        # at least 2 positioned node connected:
        if neibslen >= 2:
            Li[node] = np.array([0.0, 0.0])
            for neib in neibsi_1:
                Li[node] += Li_1[neib]
            Li[node] /= float(neibslen)
            contribution_factor[node] = contribution_factor_level[2]
        # only 1 positioned node connected:
        elif neibslen == 1:
            Li[node] = Li_1[list(neibsi_1)[0]] + dl * np.cos(np.random.uniform( 0.0,2.0*np.pi ))
            contribution_factor[node] = contribution_factor_level[1]
        # no positioned node connected:
        else:
            Li[node] = center_bx + np.random.uniform( -0.5,0.5 ) * bounding_box_size
            contribution_factor[node] = contribution_factor_level[0]

    # TODO Edge Varying Merging

    for node in Li_1:
        contribution_factor[node] = contribution_factor_level[3]

    return Li


# def Refinement():
#     Li={}
#     return Li


def Incremental(gs, C=4.0, dl=0.055, weight='weight', seed=0):
    posOut=[]
    Li=None
    for i, Gi in enumerate(gs):
        if i==0:
            Li = fm3_layout(G=Gi, C=C, dl=dl, iterations=100, weight=weight, seed=seed, scale=None)
        Li = Merging(gs[i], gs[0], Li, dl)
        Li = fm3_layout(G=Gi, pos=Li, C=C, dl=dl, iterations=100, weight=weight, seed=seed, scale=None)

        posOut.append(deepcopy(Li))
    
    for i, pos in enumerate(posOut):
        nx.set_node_attributes(G=gs[i], values=pos, name='pos')

    return gs
