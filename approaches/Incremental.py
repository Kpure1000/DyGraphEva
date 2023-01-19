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

    return Li, move_flag


def Collapse(Gk_1, move_flag,weight):
    Gk = Gk_1.copy()
    SSs = [] # solar systems
    SUN = set()
    while len(Gk) > 0:
        comps = nx.connected_components(Gk)
        S = set()
        for node_comp in comps:
            S.add(max(list(nx.degree(Gk, node_comp)), key = lambda ele: ele[1])[0])
        V = set(S)
        SUN = SUN | S
        for s in S:
            P = set(Gk.neighbors(s))
            V = V | P
            M = set()
            for p in P:
                M = M | set(Gk.neighbors(p)) - V
                V = V | M
            SSs.append(
                (s, P, M, V)
            )
        Gk.remove_nodes_from(V)
    # print(SSs)
    Gk.add_nodes_from({n: dict(Gk_1.nodes)[n] for n in SUN})
    for i in range(len(SSs)):
        for j in range(i):
            SSi, SSj, Si, Sj = SSs[i][3], SSs[j][3], SSs[i][0], SSs[j][0]
            # find edges between SSi and SSj
            dl_uv, count = 0.0, 0 # designed length
            for u in SSi:
                for v in SSj:
                    if Gk_1.has_edge(u,v):
                        dl_uv += Gk_1[u][v][weight]
                        if Gk_1.has_edge(Si, u): dl_uv += Gk_1[Si][u][weight]
                        if Gk_1.has_edge(v, Sj): dl_uv += Gk_1[v][Sj][weight]
                        count += 1
            if count > 0:
                dl_uv /= float(count)
                Gk.add_edge(Si, Sj, **{weight: dl_uv})
    # contribution factor
    contribution_factor = {}
    for ss in SSs:
        if len(ss[3]) <= 1: 
            contribution_factor[ss[0]] = 1.0 if move_flag[ss[0]] is True else 0.0
            continue
        count = 0
        for v in ss[3]:
            if ss[0] is not v and move_flag[v] is True:
                count += 1
        contribution_factor[ss[0]] = count / (len(ss[3]) - 1)
    return Gk, contribution_factor


def Multilevel(Gi, move_flag, weight):
    G0 = Gi.copy()
    Level = []
    Level.append((G0, {})) # (Gx, contribution_factor)
    Gk = G0
    while True:
        Gk, cf = Collapse(Gk, move_flag, weight)
        if len(Gk) > 1:
            Level.append((Gk, cf))
        else:
            break
    return Level


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
                min_ite=30,
                max_ite=250,
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
            Li, move_flag = Merging(gs[i], gs[i-1], Li, dl)

            Level = Multilevel(Gi, move_flag, weight)
            ite = int(min_ite + (max_ite - min_ite) / len(Level))
            for i, lv in enumerate(reversed(Level)):
                Gk = lv[0]
                Li_i = {n: Li[n] for n in Gk.nodes}
                iterations = max_ite - i * ite
                nodes_ite = {}
                for n in Gk.nodes:
                    nodes_ite[n] = iterations if n not in lv[1] else lv[1][n] * iterations
                Li_i = fm3_layout(G=Gk,
                                pos=Li_i,
                                iterations=iterations,
                                weight=weight,
                                seed=seed,
                                scale=None,
                                nodes_ite=nodes_ite,
                                C=C,
                                dl=dl)
                for n in Li_i:
                    Li[n] = Li_i[n]

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


# Multilevel Test
# G = nx.watts_strogatz_graph(100, 3, 0.8, 0)
# # G = nx.Graph([(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (7, 6), (7, 8), (9, 8),
# #               (10, 8), (11, 8), (12, 13), (12, 14), (12, 15), (12, 16),
# #               (12, 17), (16, 18), (17, 11), (3, 19), (19, 12)])
# nx.set_edge_attributes(G, 1.0, 'weight')
# L = Multilevel(G, None, None, None)
# G = L[1][0]
# lb = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx(G, pos=nx.fruchterman_reingold_layout(G, seed=0))
# # nx.draw_networkx_edge_labels(G, pos=nx.fruchterman_reingold_layout(G, seed=0),edge_labels=lb)
# plt.show()
