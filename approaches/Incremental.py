from copy import deepcopy
import networkx as nx
import numpy as np
from FM3 import fm3_layout

import matplotlib.pyplot as plt


def Merging(Gi, Gi_1, Li_1, dl):

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

    # find new nodes
    nodesi = set(Gi.nodes())        # nodes of Gi
    nodesi_1 = set(Gi_1.nodes())    # nodes of Gi-1
    nodes_new = nodesi - nodesi_1

    edgesi = set(Gi.edges())
    edgesi_1 = set(Gi_1.edges())
    edges_new = edgesi - edgesi_1
    edges_del = edgesi_1 - edgesi
    edges_var = edges_new & edges_del

    contri_fact_level = [1.0, 0.5, 0.25, 0.1]
    contri_fact={}

    move_flag = {n: False for n in nodesi}

    # neibs of all node in Gi
    neibs={}
    for node in nodesi:
        neibs[node] = list(nx.neighbors(G=Gi, n=node))

    Li = Li_1.copy()
    for node in nodes_new:
        neibsi_1 = set(neibs[node]) & nodesi_1 # neibs i-1
        neibslen = len(neibsi_1)
        # at least 2 positioned node connected:
        if neibslen >= 2:
            Li[node] = np.array([0.0, 0.0])
            for neib in neibsi_1:
                Li[node] += Li_1[neib]
                move_flag[neib] = True
            Li[node] /= float(neibslen)
            contri_fact[node] = contri_fact_level[2]
        # only 1 positioned node connected:
        elif neibslen == 1:
            rd_angle = np.random.uniform( 0.0, 2.0 * np.pi )
            Li[node] = Li_1[list(neibsi_1)[0]] + dl * np.array(np.cos(rd_angle),np.sin(rd_angle))
            contri_fact[node] = contri_fact_level[1]
            move_flag[list(neibsi_1)[0]] = True
        # no positioned node connected:
        else:
            Li[node] = center_bx + np.random.uniform( -0.5,0.5 ) * bounding_box_size
            contri_fact[node] = contri_fact_level[0]
        move_flag[node] = True

    for edge_var in edges_var:
        u = edge_var[0]
        v = edge_var[1]
        if u in nodes_new and v in nodes_new:
            if move_flag[v] is False:
                if move_flag[u] is False:
                    Li[u] = center_bx + np.random.uniform( -0.5,0.5 ) * bounding_box_size
                    move_flag[u] = True
                rd_angle = np.random.uniform( 0.0, 2.0 * np.pi )
                Li[v] = Li[u] + dl * np.array(np.cos(rd_angle),np.sin(rd_angle))
                move_flag[v] = True
            else:
                if move_flag[u] is False:
                    rd_angle = np.random.uniform( 0.0, 2.0 * np.pi )
                    Li[u] = Li[v] + dl * np.array(np.cos(rd_angle),np.sin(rd_angle))
                    move_flag[u] = True
        elif u not in nodes_new and v not in nodes_new:
            move_flag[u] = move_flag[v] = True
            continue
        else:
            if u not in nodes_new and v in nodes_new:
                u = edge_var[1]
                v = edge_var[0]
                move_flag[u] = True
                if move_flag[v] is True:
                    continue
                rd_angle = np.random.uniform( 0.0, 2.0 * np.pi )
                Li[v] = Li[u] + dl * np.array(np.cos(rd_angle),np.sin(rd_angle))
                move_flag[v] = True

    for node in nodes_new:
        move_flag[node] = True

    for node in Li_1:
        contri_fact[node] = contri_fact_level[3]

    return Li, move_flag, neibs


def Multilevel(Gi, Li, move_flag, neibs, min_ite=30, max_ite=250):
    comps = nx.connected_components(Gi)
    super_nodes = []
    for node_set in comps:
        super_nodes.append(max(list(nx.degree(Gi, node_set)), key = lambda ele: ele[1])[0])
    nodes_ite = dict()
    contri_facts = {}
    for n in super_nodes:
        nodes_ite[n] = 0
        cf = 0
        for nei in neibs[n]:
            if move_flag[nei] == True:
                cf += 1
        if cf == 0:
            contri_facts[n] = 0
        else:
            contri_facts[n] = float(cf / len(neibs[n]))
    # bfs
    que = super_nodes.copy()
    while len(que) > 0:
        rear_n = que[0]
        for nei in neibs[rear_n]:
            if nei not in nodes_ite:
                que.append(nei)
                nodes_ite[nei] = nodes_ite[rear_n] + 1
        que.pop(0)

    max_level = max([nodes_ite[n] for n in nodes_ite])
    if max_level == 0:
        for n in super_nodes:
            nodes_ite[n] = 250
        return nodes_ite

    d_level = float(max_ite - min_ite) / (max_level)

    for n in nodes_ite:
        nodes_ite[n] = int(
            (max_ite - d_level * (nodes_ite[n]))
        )

    for n in super_nodes:
        nodes_ite[n] *= contri_facts[n]

    return nodes_ite


def Refinement(Gi, Li, C, dl, weight, K=1.0):
    pos = np.array([np.asarray(Li[n]) for n in Li])

    A = nx.to_numpy_array(G=Gi, weight=weight)
    pos = pos.astype(A.dtype)

    # delta = np.zeros((pos.shape[0], pos.shape[0], pos.shape[1]), dtype=A.dtype)

    _1d9 = 1.0 / 9.0
    dl3 = dl * dl * dl
    ones = np.ones((A.shape[0], A.shape[1]))

    delta = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]

    # distance between points
    distance = np.linalg.norm(delta, axis=-1)
    # enforce minimum distance of 0.01
    np.clip(distance, 0.01, None, out=distance)
    En = np.einsum(
        "ij,ij->i", ones, -C / distance +
            A * _1d9 * (distance**3 * (np.log(distance / dl) - 1) + dl3)
    )

    miu = np.mean(En)

    refine = {n: (abs(En[i] - miu) / miu > K) for i, n in enumerate(Li)}

    return refine


def Incremental(gs,
                C=4.0,
                dl=0.055,
                K=1.0,
                max_ite=250,
                min_ite=30,
                re_ite=20,
                weight='weight',
                seed=0):
    posOut=[]
    Li=None
    for i, Gi in enumerate(gs):
        if i == 0:
            Li = fm3_layout(G=Gi,
                            iterations=max_ite,
                            weight=weight,
                            seed=seed,
                            scale=None,
                            C=C,
                            dl=dl)
        else:
            Li, move_flag, neibs = Merging(gs[i], gs[i-1], Li, dl)
            nodes_ite = Multilevel(Gi, Li, move_flag, neibs, min_ite, max_ite)
            Li = fm3_layout(G=Gi,
                            pos=Li,
                            iterations=max_ite,
                            weight=weight,
                            seed=seed,
                            scale=None,
                            C=C,
                            dl=dl,
                            nodes_ite=nodes_ite)
            refine = Refinement(Gi, Li, C, dl, weight, K)
            fixed = [n for n in refine if refine[n] == False]
            if len(fixed) == 0: fixed = None
            Li = fm3_layout(G=Gi,
                            pos=Li,
                            iterations=re_ite,
                            weight=weight,
                            seed=seed,
                            scale=None,
                            C=C,
                            dl=dl,
                            fixed=fixed)

        posOut.append(deepcopy(Li))

    for i, pos in enumerate(posOut):
        nx.set_node_attributes(G=gs[i], values=pos, name='pos')

    return gs
