from copy import deepcopy
from json import dumps
import pickle
from app_total import read_Graphs
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

from app_total import save_Graphs


# gs, distance_scale = read_Graphs("../data/dataset/synth/test0/", "test")
gs, distance_scale = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
# gs, distance_scale = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")
# gs, distance_scale = read_Graphs("../data/dataset/synth/node_add/", "node_add")
# gs, distance_scale = read_Graphs("../data/dataset/synth/cube/", "cube")


def Aging(Gi, Gi_1=None, Ai_1=None):
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


def Age_drag_index(Ages_G):
    #param
    beta = 0.5

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
    for i in range(0, len(gs)):
        if i == 0:
            Ai = Aging(Gi=gs[i])
        else:
            Ai = Aging(Gi=gs[i], Gi_1=gs[i-1], Ai_1=Ai)
        Ages[gs[i]] = deepcopy(Ai)
    return Ages


def fd_iterator(G, drag_index, k=None, init_pos=None, distance_scale=1.0, iterator_count=50, pos_rec=None):

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
                weight = G.get_edge_data(nodes[s], nei_s[n])['weight']
                F_attr += x_sn * np.sqrt(x_sn.dot(x_sn)) / k / (1 + weight * distance_scale)
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


def OnlineDraw(ax, Gi,drag_index, Li_1=None):
    if Li_1!=None:
        # Li = nx.fruchterman_reingold_layout(G=Gi, pos=Li_1)
        Li = fd_iterator(G=Gi,drag_index=drag_index, init_pos=Li_1)
        # Li = fd_iterator(G=Gi,drag_index=drag_index)
    else:
        # Li = nx.fruchterman_reingold_layout(Gi)
        Li = fd_iterator(G=Gi,drag_index=drag_index)

    nx.draw_networkx(
        G=Gi,
        pos=Li,
        node_size=35,
        node_shape="o",
        edge_color="#aaa",
        width=1.5,
        font_size=4,
        font_color="#fff",
        ax=ax
    )

    return Li


np.random.seed(1)

Ages_G = Aging_Gs(Gs=gs)

drag_index_G = Age_drag_index(Ages_G=Ages_G)

glen = len(gs)
fig, ax = plt.subplots(nrows=1, ncols=glen)
Li_1=None
axr=list(ax)
axc=list(axr)
posOut=[]
for i in range(0, glen):
    axc[i].set_xlim(-2.0,2.0)
    axc[i].set_ylim(-2.0,2.0)
    if i==0:
        Li_1 = OnlineDraw(ax=axc[i],drag_index=drag_index_G[gs[i]], Gi=gs[i])
        posOut.append(deepcopy(Li_1))
    else:
        Li_1 = OnlineDraw(ax=axc[i],drag_index=drag_index_G[gs[i]], Gi=gs[i], Li_1=Li_1)
        posOut.append(deepcopy(Li_1))

plt.show()

for i in range(0, len(posOut)):
    nx.set_node_attributes(G=gs[i], values=posOut[i], name='pos')

# save_Graphs("../data/result/synth/node_add/", "node_add", gs, distance_scale)
save_Graphs("../data/result/synth/newcomb/", "newcomb", gs, distance_scale)
# save_Graphs("../data/result/synth/test/", "test", gs, distance_scale)
