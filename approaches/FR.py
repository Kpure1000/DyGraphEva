from cmath import isnan
from copy import deepcopy
from app_total import read_Graphs
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

# gs, distance_scale = read_Graphs("../data/dataset/synth/test0/", "test")
# gs, distance_scale = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
# gs, distance_scale = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")
# gs, distance_scale = read_Graphs("../data/dataset/synth/cube/", "cube")

# np.random.seed(0)

def fr_iterator(G, k=None, init_pos=None, distance_scale=1.0, iterator_count=50, pos_rec=None):

    nodes = list(G.nodes)

    # param
    nodelen = len(nodes)
    if k == None: k = np.sqrt(1 / nodelen)
    drag_index = 0.55
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
            # node_pos[nodes[s]] += drag_index * v_s * min(temperature, F_tot_mag)
            node_pos[nodes[s]] += v_s * min(temperature, F_tot_mag)
        temperature *= lambda_
        if pos_rec!=None:
            pos_rec.append(deepcopy(node_pos))

    return node_pos

# pos_out=[]

# fr_iterator(G=gs[0], pos_rec=pos_out)

# fig = plt.figure()
# fig.set_size_inches(5, 5)
# plt.xlim(-1., 1.)
# plt.ylim(-1., 1.)
# plt.get_current_fig_manager().set_window_title("force-directed test")


# def drawg(pos):
#     plt.cla()
#     nx.draw_networkx(
#         G=gs[0],
#         pos=pos,
#         node_size=80,
#         node_shape="s",
#         edge_color="#aaa",
#         width=1.5,
#         font_size=6,
#         font_color="#fff",
#     )


# anim = ani.FuncAnimation(fig=fig,
#                          func=drawg,
#                          frames=pos_out,
#                          interval=33,
#                          repeat=True,)

# plt.show()
