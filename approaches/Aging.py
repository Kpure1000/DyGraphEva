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
                    # print("{0}: {1}".format(node, Neib_add))
                    for neib in Neib_rem:
                        A_rem += Ai_1[neib]
                    for neib in Neib_del:
                        A_del += Ai_1[neib]
                    for neib in Neib_add:
                        if neib in Ai_1:
                            A_add += Ai_1[neib]
                    A_tot = A_rem + A_del + A_add
                    Ai[node] = Ai_1[node] * (A_rem / A_tot) + 1.0
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


def fd_iterator(G, drag_index, k=None, init_pos=None, distance_scale=1.0, iterator_count=50, pos_rec=None, weight='weight'):

    nodes = list(G.nodes)

    # param
    nodelen = len(nodes)
    if k == None: k = np.sqrt(1 / nodelen)
    lambda_ = 0.9
    temperature = k * np.sqrt(nodelen)

    # pre-compute neighbors
    neighbors={}
    for node in nodes:
        neighbor = nx.neighbors(G, node)
        neighbors[node]=list(neighbor)

    # initial position
    node_pos={}
    for i in range(0, nodelen):
        node_pos[nodes[i]] = (
            (np.random.rand() - 0.5) * 0.1,
            (np.random.rand() - 0.5) * 0.1
        )
    if init_pos != None:
        for node in init_pos:
            node_pos[node] = init_pos[node]

    # iterate
    for it in range(0, iterator_count):
        # barycentric
        barycentric = 0
        for i in nodes:
            barycentric += np.array(node_pos[i])
        barycentric /= nodelen
        # each node
        for s in range(0, nodelen):
            nei_s = neighbors[nodes[s]]
            F_attr = np.array([0.0,0.0])
            for n in range(0, len(nei_s)):
                x_s = np.array(node_pos[nodes[s]])
                x_n = np.array(node_pos[nei_s[n]])
                x_sn = x_n - x_s
                w = G.get_edge_data(nodes[s], nei_s[n])[weight]
                F_attr += x_sn * np.sqrt(x_sn.dot(x_sn)) / k  / (1 + w * distance_scale)
                # F_attr += x_sn * np.sqrt(x_sn.dot(x_sn)) / k  * weight * distance_scale
            F_repl = np.array([0.0,0.0])
            for n in range(0, nodelen):
                if n != s:
                    x_s = np.array(node_pos[nodes[s]])
                    x_n = np.array(node_pos[nodes[n]])
                    x_ns = x_s - x_n
                    F_repl += k * k * x_ns / x_ns.dot(x_ns)
            F_tot = F_attr + F_repl
            F_tot_mag = np.sqrt(F_tot.dot(F_tot))
            v_s = F_tot / (F_tot_mag)
            node_pos[nodes[s]] += drag_index[node] * v_s * min(temperature, F_tot_mag)
            # node_pos[nodes[s]] += v_s * min(temperature, F_tot_mag)
        temperature *= lambda_
        if pos_rec!=None:
            pos_rec.append(deepcopy(node_pos))

    return node_pos

def Aging(gs, beta=1, weight='weight', seed=1):
    np.random.seed(seed)
    Ages_G = Aging_Gs(Gs=gs)
    drag_index_G = Age_drag_index(Ages_G=Ages_G, beta=beta)

    posOut=[]
    Li_1=None
    for i in range(0, len(gs)):
        if i==0:
            Li_1 = nx.kamada_kawai_layout(G=gs[i], weight=weight)
            Li_1 = fr_layout(G=gs[i],
                             pos=Li_1,
                             weight=weight,
                             k=0.1,
                             drag_index=drag_index_G[gs[i]]
                             )
        else:
            Li_1 = fr_layout(G=gs[i],
                             pos=Li_1,
                             weight=weight,
                             k=0.1,
                             drag_index=drag_index_G[gs[i]]
                             )
        posOut.append(deepcopy(Li_1))

    for i in range(0, len(posOut)):
        nx.set_node_attributes(G=gs[i], values=posOut[i], name='pos')

    return gs
