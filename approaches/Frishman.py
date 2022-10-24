from copy import deepcopy
from json import dumps
import pickle
from app_total import read_Graphs
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

def Merging(Gi, Gi_1, Li_1):
    # merging params
    circle_scale = 0.1
    score_level = {1: 1.0, 2: 0.25, 3: 0.1, 4: 0.0}

    # find added nodes
    nodesi = set(Gi.nodes())     # nodes of Gi
    nodesi_1 = set(Gi_1.nodes()) # nodes of Gi-1
    added_nodes = nodesi - nodesi_1

    # bounding box of Li-1
    bounding_box = [
        np.array([float('inf'), float('inf')]),  # min
        np.array([float('-inf'), float('-inf')]),  # max
    ]
    for node in Li_1:
        bounding_box[0][0] = min(bounding_box[0][0], Li_1[node][0])
        bounding_box[0][1] = min(bounding_box[0][1], Li_1[node][1])
        bounding_box[1][0] = max(bounding_box[1][0], Li_1[node][0])
        bounding_box[1][1] = max(bounding_box[1][1], Li_1[node][1])

    # center of bounding box
    center_bx = 0.5 * ( bounding_box[0] + bounding_box[1] )
    bounding_box_size = bounding_box[1] - bounding_box[0]
    # radius of center circle (layout nodes without exist neighbor)
    radius = circle_scale * min(bounding_box_size[0], bounding_box_size[1]) * 0.5

    # compute Li, score
    neibs={} # neibs of all node in Gi
    for node in nodesi:
        neibs[node] = list(nx.neighbors(G=Gi, n=node))

    neibs_newNode={} # the neighbors, existed in Gi-1, of new nodes
    Li={}
    score={}
    for node in added_nodes:
        neib_set = set(neibs[node]) & nodesi_1
        neibs_newNode[node] = neib_set
        neibslen = len(neib_set)
        if neibslen >= 2:
            Li[node] = np.array([0.0, 0.0])
            for neib in neib_set:
                Li[node] += Li_1[neib]
            Li[node] /= neibslen
            score[node]= score_level[2]
        elif neibslen == 1:
            # along the line of neighbor and bounding box center
            line_ratio = np.random.random()
            Li[node] = line_ratio * Li_1[list(neib_set)[0]] + ( 1 - line_ratio ) * center_bx
            score[node]= score_level[3]
        else:
            Li[node] = center_bx  + [
                radius * np.cos(2 * np.pi * np.random.random()),
                radius * np.sin(2 * np.pi * np.random.random()),
            ]
            score[node]= score_level[4]

    # union All nodes in Li and score
    for nodeOld in Li_1:
        Li[nodeOld]=Li_1[nodeOld]
        score[nodeOld]=score_level[1]

    return deepcopy(Li), score, neibs


def Pinning(Gi, Gi_1, score, neibs):
    # Pining params
    alpha=0.6
    Wpin_init = 0.35
    k=0.5

    nodes = list(Gi.nodes)
    Wpin_local = {}
    for node in nodes:
        if len(neibs[node]) > 0:
            scoreNeib=0
            for neib in neibs[node]:
                scoreNeib += score[neib]
            degree = nx.degree(G=Gi, nbunch=node, weight='weight')
            Wpin_local[node] = alpha * score[node] + (1 - alpha) * scoreNeib / degree
        else:
            Wpin_local[node] = alpha * score[node]

    # print("Wpin_local: {0}".format(Wpin_local))

    D0=set()
    edge_rm = set(Gi_1.edges) - set(Gi.edges)
    edge_add = set(Gi.edges) - set(Gi_1.edges)
    # nodes with low Wpin (< 1.0)
    for node in Wpin_local:
        if Wpin_local[node] < 1.0:
            # print("wpin[{0}] = {1} < 1.0".format(node, Wpin_local[node]))
            D0.add(node)
    # nodes with removed edges
    for rm in edge_rm:
        # print("rm node[{0}]".format(rm))
        D0.add(rm[0])
        D0.add(rm[1])
    # nodes with added edges
    for add in edge_add:
        # print("add node[{0}]".format(add))
        D0.add(add[0])
        D0.add(add[1])

    Ds={0:D0}
    dmax=0
    Di = set()
    Di_1=D0

    while True:
        Di.clear()
        for node in Di_1:
            for neib in neibs[node]:
                is_in = False
                for D in Ds:
                    if neib in Ds[D]:
                        is_in=True
                if not is_in:
                    Di.add(neib)
        if len(Di) > 0:
            dmax += 1
            Ds[dmax] = Di.copy()
            Di_1=Ds[dmax]
        else:
            break

    # print(Ds)

    Ds_list = list(Ds)
    Wpin_global=Wpin_local
    dcutoff = k * dmax
    # i[0,0]=Wpin_init, i[1,Ddcutoff]=pwr, i(dcutoff,)=1
    for i in range(0, dmax + 1):
        for node in Ds[Ds_list[i]]:
            if i == 0 or int(dcutoff) == 0.0:
                Wpin_global[node] = Wpin_init
            elif i > int(dcutoff):
                Wpin_global[node] = 1.0
            else:
                Wpin_global[node] = np.power(Wpin_init, 1 - i / dcutoff)

    # print("Wpin_global: {0}".format(Wpin_global))

    return Wpin_global


def FrLayout(Gi, Li, neibs, wpin_glob=None, distance_scale=1.0):
    nodes=list(Gi.nodes)
    nodelen=len(nodes)
    # FrLayout params
    drag_index = 0.55
    area = 0.2
    Fr_k = 0.1 #np.sqrt(area/nodelen)
    lambda_ = 0.9
    temperature = Fr_k * np.sqrt(nodelen)
    iterator_times=50

    frac_done=0
    node_pos=Li
    for it in range(1, iterator_times + 1):
        # each node
        for s in range(0, nodelen):
            # if wpin_glob != None: print("node[{0}]: frac_done={1}, wpin={2}".format(nodes[s], frac_done, wpin_glob[nodes[s]]))
            if (wpin_glob != None and frac_done > wpin_glob[nodes[s]]) or (wpin_glob == None):
                nei_s = neibs[nodes[s]]
                F_attr = np.array([0.0,0.0])
                for n in range(0, len(nei_s)):
                    x_s = np.array(node_pos[nodes[s]])
                    x_n = np.array(node_pos[nei_s[n]])
                    x_sn = x_n - x_s
                    weight = Gi.get_edge_data(nodes[s], nei_s[n])['weight']
                    F_attr += x_sn * np.sqrt(x_sn.dot(x_sn)) / Fr_k / (1 + weight * distance_scale)
                F_repl = np.array([0.0,0.0])
                for n in range(0, nodelen):
                    if n != s:
                        x_s = np.array(node_pos[nodes[s]])
                        x_n = np.array(node_pos[nodes[n]])
                        x_ns = x_s - x_n
                        F_repl += Fr_k * Fr_k * x_ns / x_ns.dot(x_ns)
                F_tot = F_attr + F_repl
                F_tot_mag = np.sqrt(F_tot.dot(F_tot))
                # node_pos[nodes[s]] += drag_index * F_tot / (F_tot_mag) * min(temperature, F_tot_mag)
                node_pos[nodes[s]] += F_tot / (F_tot_mag) * min(temperature, F_tot_mag)

        temperature *= lambda_
        frac_done += 1 / it

    return node_pos


def InitLayout(G0, distance_scale):
    # 1) TODO: coarsening
    # 2) perform kk layout
    L0 = nx.kamada_kawai_layout(G=G0)
    neibs={} # neibs of all node in Gi
    for node in G0.nodes:
        neibs[node] = list(nx.neighbors(G=G0, n=node))
    L0 = FrLayout(Gi=G0, Li=L0, neibs=neibs, distance_scale=distance_scale)
    return L0


def OnlineLayout(Gi, Gi_1, Li_1, distance_scale):
    # 1) Merging: Merge layout Li-1 and graph Gi to produce an initial layout.
    Li_init, score, neibs = Merging(Gi, Gi_1, Li_1)
    Wpin_glob = Pinning(Gi, Gi_1, score, neibs)

    Li = FrLayout(Gi, Li_init, neibs, wpin_glob=Wpin_glob, distance_scale=distance_scale)

    return Li


def Frishman(gs, distance_scale):
    np.random.seed(1)

    Li_1 = None
    posOut=[]
    for i in range(0, len(gs)):
        if i == 0:
            Li_1 = InitLayout(G0=gs[i], distance_scale=distance_scale)
        else:
            Li_1 = OnlineLayout(Gi=gs[i], Gi_1=gs[i - 1], Li_1=Li_1, distance_scale=distance_scale)
        posOut.append(deepcopy(Li_1))

    for i in range(0, len(posOut)):
        nx.set_node_attributes(G=gs[i], values=posOut[i], name='pos')

    return gs
