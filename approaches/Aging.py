from copy import deepcopy
import networkx as nx
import numpy as np
from FR import fr_layout

def Aging_g(Gi, Gi_1=None, Ai_1=None):
    Ai = {}
    if Ai_1 != None and Gi_1 != None:
        for node in Gi:
            Neib = set(Gi.neighbors(node))
            Neib_1=set()
            if node in Gi_1:
                Neib_1 = set(Gi_1.neighbors(node))
                if len(Neib) > 0:
                    A_rem = 0.0
                    A_del = 0.0
                    A_add = 0.0
                    Neib_rem = Neib & Neib_1
                    Neib_del = Neib_1 - Neib
                    Neib_add = Neib - Neib_1
                    for neib in Neib_rem:
                        A_rem += Ai_1[neib]
                    for neib in Neib_del:
                        A_del += Ai_1[neib]
                    for neib in Neib_add:
                        if neib in Ai_1:
                            A_add += Ai_1[neib]
                    A_tot = A_rem + A_del + A_add
                    if A_tot > 0:
                        Ai[node] = Ai_1[node] * (A_rem / A_tot) + 1.0
                    else:
                        Ai[node] = Ai_1[node] + 1.0
                    # Ai[node] = Ai_1[node] * np.floor(A_rem / A_tot) + 1.0
                else:
                    Ai[node] = Ai_1[node] + 1.0
            else:
                Ai[node] = 1.0
    else:
        for node in Gi:
            Ai[node] = 1.0

    return Ai


def Age_drag_index(Ages_G, beta):
    #param
    # beta = 2.5

    drag_index_G={}
    for G in Ages_G:
        drag_node = {}
        Age = Ages_G[G]
        for node in Age:
            drag_node[node] = np.power( np.e , - beta * Age[node])
        drag_index_G[G] = drag_node

    return drag_index_G


def Aging_Gs(Gs):
    Ages={}
    for i in range(0, len(Gs)):
        if i == 0:
            Ai = Aging_g(Gi=Gs[i])
        else:
            Ai = Aging_g(Gi=Gs[i], Gi_1=Gs[i-1], Ai_1=Ai)
        Ages[Gs[i]] = deepcopy(Ai)
    return Ages


def Aging(gs, beta=1, k=0.1, iterations=100, weight='weight', seed=1):
    np.random.seed(seed)
    Ages_G = Aging_Gs(Gs=gs)
    drag_index_G = Age_drag_index(Ages_G=Ages_G, beta=beta)

    posOut=[]
    Li_1=None
    # for i in range(0, len(gs)):
    for i, G in enumerate(gs):
        # if i==0:
        # Li_1 = nx.kamada_kawai_layout(G=G, weight=weight)
        from FM3 import fm3_layout
        Li_1 = fr_layout(G=G,
                         pos=Li_1,
                         weight=weight,
                         k=k,
                         iterations = iterations,
                         drag_index=drag_index_G[G],
                         scale=None
                         )

        posOut.append(deepcopy(Li_1))

    for i, pos in enumerate(posOut):
        nx.set_node_attributes(G=gs[i], values=pos, name='pos')

    return gs
