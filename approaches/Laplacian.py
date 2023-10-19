import networkx as nx
import numpy as np
import scipy as sp
import random

from FR import fr_layout
from app_total import read_Graphs

# lap_pos = []


def Merging(Gi, Gi_1, Li_1):
    nodesi = set(Gi.nodes())        # nodes of Gi
    nodesi_1 = set(Gi_1.nodes())    # nodes of Gi-1
    nodes_new = nodesi - nodesi_1
    nodes_mutual = nodesi & nodesi_1

    # bounding_box
    bd_box = [
        np.array([float('inf'), float('inf')]),  # min
        np.array([float('-inf'), float('-inf')]),  # max
    ]
    for node in Li_1:
        bd_box[0][0] = min(bd_box[0][0], Li_1[node][0])
        bd_box[0][1] = min(bd_box[0][1], Li_1[node][1])
        bd_box[1][0] = max(bd_box[1][0], Li_1[node][0])
        bd_box[1][1] = max(bd_box[1][1], Li_1[node][1])
    pos_x_min = bd_box[0][0]
    pos_y_min = bd_box[0][1]
    pos_x_max = bd_box[1][0]
    pos_y_max = bd_box[1][1]

    #average edge length
    avg_edge_l = .0
    edges = set(Gi_1.edges())
    for e in edges:
        avg_edge_l += np.linalg.norm(Li_1[e[0]] - Li_1[e[1]])
    avg_edge_l /= len(edges)

    Li={}

    for node in nodes_mutual:
        Li[node] = Li_1[node]

    for node in nodes_new:
        neibs_list_Gi = set(nx.neighbors(G=Gi, n=node))
        neibs_list_Gi_1 = set(Gi_1.nodes())
        if len(neibs_list_Gi & neibs_list_Gi_1) == 1:
            p = list(neibs_list_Gi)[0]
            p_pos = Li_1[p]
            theta = random.random() * np.pi * 2.0
            Li[node] = p_pos + np.array([np.cos(theta),np.sin(theta)]) * avg_edge_l
        elif len(neibs_list_Gi & neibs_list_Gi_1) > 1:
            num_neibs = len(neibs_list_Gi & neibs_list_Gi_1)
            sum_pos = np.array([0.0, 0.0])
            for neib in (neibs_list_Gi & neibs_list_Gi_1):
                sum_pos += Li_1[neib]
            Li[node] = sum_pos / num_neibs
        else:
            Li[node] = np.array([random.random() * (pos_x_max - pos_x_min) + pos_x_min,
                                 random.random() * (pos_y_max - pos_y_min) + pos_y_min])

    return Li


def Refinement(Gi, Gi_1, Li_1, L_star, alpha):
    pos_arr = np.array([L_star[l] for l in L_star])

    nodes_s_i = set(Gi.nodes)
    nodes_s_i_1 = set(Gi_1.nodes)
    nodes_both = nodes_s_i & nodes_s_i_1

    nNodes = len(Gi)
    d_star_mat_inv = np.zeros((nNodes, nNodes))
    d_i_1_mat_inv = np.zeros((nNodes, nNodes))
    for u, nu in enumerate( Gi ):
        for v, nv in enumerate( Gi ):
            if u != v:
                if Gi.has_edge(nu, nv):
                    d_star_mat_inv[u, v] = 1.0 / (np.linalg.norm(L_star[nu] - L_star[nv]) + 1e-3)
                if nu in nodes_both and nv in nodes_both:
                    d_i_1_mat_inv[u, v] = 1.0 / (np.linalg.norm(Li_1[nu] - Li_1[nv]) + 1e-3)

    args = (d_star_mat_inv, d_i_1_mat_inv, alpha)
    opres = sp.optimize.minimize(
        EnergyFn,
        pos_arr.ravel(),
        # method="CG",
        method="L-BFGS-B",
        args=args,
        jac=True
    )

    # print(f'n_nodes: {nNodes}, n_its: {opres.nfev}')

    pos = opres.x.reshape((-1, 2))
    Li = dict(zip(Gi, pos))
    return Li


def EnergyFn(pos_vec, d_star_mat_inv, d_i_1_mat_inv, alpha):
    nNodes = d_star_mat_inv.shape[0]
    pos_arr = pos_vec.reshape((nNodes, 2))

    delta = pos_arr[:, np.newaxis, :] - pos_arr[np.newaxis, :, :]
    node_dis = np.linalg.norm(delta, axis=-1) # Djk
    dir = np.einsum("ijk,ij->ijk", delta, 1.0 / (node_dis + np.eye(nNodes) * 1e-3))

    offset1 = node_dis * d_star_mat_inv - 1.0 # Djk / djk - 1, (j,k) is in Gi.edges
    offset2 = node_dis * d_i_1_mat_inv - 1.0  # Djk / djk - 1, j and k are in both Gi and Gi_1
    offset1[np.diag_indices(nNodes)] = 0
    offset2[np.diag_indices(nNodes)] = 0

    E = np.sum(offset1**2) + alpha * np.sum(offset2**2)

    grad1 = 2 * ( np.einsum("ij,ij,ijk->ik", d_star_mat_inv, offset1, dir) - np.einsum(
                            "ij,ij,ijk->jk", d_star_mat_inv, offset1, dir) )
    grad2 = 2 * ( np.einsum("ij,ij,ijk->ik", d_i_1_mat_inv,  offset2, dir) - np.einsum(
                            "ij,ij,ijk->jk", d_i_1_mat_inv,  offset2, dir) )

    # print(f'+ {E}')
    # lap_pos.append(pos_arr)

    grad = grad1 + alpha * grad2

    return E, grad.ravel()


def Laplacian(gs, weight='weight', seed=0, iterations=100, alpha=10.0):
    from copy import deepcopy
    posOut = []
    for i, Gi in enumerate(gs):
        if i == 0:
            Li = fr_layout(G=Gi,
                           weight=weight,
                           seed=seed,
                           iterations=iterations,
                           scale=None)
        else:
            Li_1 = Li
            Li_merge = Merging(Gi,gs[i-1],Li_1)
            L_star = fr_layout(G=Gi,
                           pos=Li_merge,
                           weight=weight,
                           seed=seed,
                           iterations=iterations,
                           scale=None)
            Li = Refinement(Gi=Gi,
                            Gi_1=gs[i - 1],
                            Li_1=Li_1,
                            L_star=L_star,
                            alpha=alpha)
            # Li = L_star
        posOut.append(deepcopy(Li))

    for i, pos in enumerate(posOut):
        nx.set_node_attributes(G=gs[i], values=pos, name='pos')

    return gs


# Testing follow Fig.1 & Fig.2 in paper

# G0 = nx.Graph([(0, 1), (1, 2), (3, 0), (2, 3)])
# G1 = nx.Graph([(0, 1), (1, 2), (3, 0), (3, 7), (7, 6), (6, 5), (5, 4), (4, 2)])
# nx.set_edge_attributes(G0, 1.0, 'weight')
# nx.set_edge_attributes(G1, 1.0, 'weight')

# Laplacian([G0, G1],iterations=250,alpha=3.0)

# import matplotlib.pyplot as plt
# import matplotlib.animation as ani

# fig = plt.figure()
# plt.axis('off')
# def aniFunc(f):
#     fig.clear()
#     nx.draw_networkx(G=G1,pos=dict(zip(G1,f)))
# a = ani.FuncAnimation(fig=fig, func=aniFunc, frames=lap_pos,repeat=True)
# a.save('lap.gif')
# plt.show()
