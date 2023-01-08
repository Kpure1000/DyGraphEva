import networkx as nx
import numpy as np
import scipy as sp

from FR import fr_layout
from app_total import read_Graphs


def Merging(Gi, Gi_1, Li_1):
    nodesi = set(Gi.nodes())        # nodes of Gi
    nodesi_1 = set(Gi_1.nodes())    # nodes of Gi-1
    nodes_new = nodesi - nodesi_1

    #average edge length
    for p in Li_1:
        p[]

    Li = {}
    for node in nodesi:
        if node in nodesi_1:
            Li[node] = Li_1[node]
        else:
            neibs_i = nx.neighbors(Gi, node)
            # if len(neibs_i) == 1:
                # Li[node] = Li_1[node] + 

    return Li


def Refinement(Gi, Gi_1, Li):
    return Li


def LCDE(Gs, weight='weight', seed=0):
    for i, Gi in enumerate(Gs):
        if i == 0:
            Li = fr_layout(G=Gi,
                           weight=weight,
                           seed=seed,
                           scale=None)
        else:
            Li = Merging(Gi,Gs[i-1],Li)
            Li = fr_layout(G=Gi,
                           pos=Li,
                           weight=weight,
                           seed=seed,
                           scale=None)
            Li = Refinement(Gi, Gs[i-1],Li)
