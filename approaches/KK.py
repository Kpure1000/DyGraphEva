from copy import deepcopy
from app_total import read_Graphs
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!! The graph must be connected graph in KK !!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# gs, distance_scale = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
gs, distance_scale = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")
# gs, distance_scale = read_Graphs("../data/dataset/synth/cube/", "cube")
g = gs[0]

nodes = list(g.nodes)

node_pos={}
# np.random.seed(0)
# initial position
nodelen = len(nodes)
for i in range(0, nodelen):
    node_pos[nodes[i]] = np.array([
        (np.random.rand() - 0.5) * 0.1,
        (np.random.rand() - 0.5) * 0.1
    ])

d_pairs={}
d_max=0
for x in range(0, nodelen):
    for y in range(0, nodelen): # allow symmetric repeat
        if y != x:
            d_xy = 0
            try:
                d_xy = nx.shortest_path_length(g,
                                               source=nodes[x],
                                               target=nodes[y],
                                               weight="weight")
            except:
                print("KK Error: Unconnected Graph Cannot Generate KK Layout")
                quit()
            d_pairs[(nodes[x], nodes[y])] = d_xy
            if d_xy > d_max:
                d_max = d_xy


L0 = 10
L = L0 / d_max
K = 0.01

l_pairs={}
k_pairs={}
for pair in d_pairs:
    d_pair = d_pairs[pair]
    l_pairs[pair] = L * d_pair
    k_pairs[pair] = K / (d_pair * d_pair)

posout=[]

max_delta = 1
err = K/10

def iterate():
    while True:
        # compute max deltaM
        dEdx = {} # dE/dx
        dEdy = {} # dE/dy
        delta_m = {}
        max_delta= 0
        mof_max_delta_m = 0
        for m in nodes:
            dEdx[m]=0
            dEdy[m]=0
            delta_m[m]=0
            for i in nodes:
                if i != m:
                    kmi = k_pairs[(m, i)]
                    lmi = l_pairs[(m, i)]
                    Xmi = node_pos[m][0] - node_pos[i][0]
                    Ymi = node_pos[m][1] - node_pos[i][1]
                    pw  =      np.power( Xmi * Xmi + Ymi * Ymi , 0.5)
                    dEdx[m] += kmi * ( Xmi - lmi * Xmi / pw )
                    dEdy[m] += kmi * ( Ymi - lmi * Ymi / pw )
            delta_m[m] = np.sqrt( dEdx[m] * dEdx[m] + dEdy[m] * dEdy[m] )
            if max_delta < delta_m[m]:
                max_delta = delta_m[m]
                mof_max_delta_m = m

        cur_delta_m = max_delta

        print("node[{0}] with max deltaM = {1}".format(mof_max_delta_m, cur_delta_m))

        if max_delta < err:
            print("final delta_m: {0}".format(delta_m))
            break

        # compute sigX, sigY
        while cur_delta_m > err:
            d2Edx2_m = 0  # d2E/dx2
            d2Edxdy_m = 0  # d2E/dxdy
            d2Edydx_m = 0  # d2E/dydx
            d2Edy2_m = 0  # d2E/dy2
            for i in nodes:
                if i != mof_max_delta_m:
                    kmi = k_pairs[(mof_max_delta_m, i)]
                    lmi = l_pairs[(mof_max_delta_m, i)]
                    Xmi = node_pos[mof_max_delta_m][0] - node_pos[i][0]
                    Ymi = node_pos[mof_max_delta_m][1] - node_pos[i][1]
                    pw =    np.power(Xmi * Xmi + Ymi * Ymi, 1.5)
                    d2Edx2_m   += kmi * (1 - lmi * Ymi * Ymi / pw)
                    d2Edxdy_m  += kmi * lmi * Xmi * Ymi / pw
                    d2Edy2_m   += kmi * (1 - lmi * Xmi * Xmi / pw)
                    d2Edydx_m  += d2Edxdy_m

            A = d2Edx2_m
            B = d2Edxdy_m
            C = d2Edydx_m
            D = d2Edy2_m
            E = dEdx[mof_max_delta_m]
            F = dEdy[mof_max_delta_m]
            H = A * D - B * C
            sigX = ( B * F - D * E ) / (  H )
            sigY = ( A * F - C * E ) / ( -H )
            # node_pos[mof_max_delta_m] += np.array([sigX, sigY])
            node_pos[mof_max_delta_m][0] += sigX
            node_pos[mof_max_delta_m][1] += sigY

            # re compute current deltaM
            dEdx[mof_max_delta_m] = 0
            dEdy[mof_max_delta_m] = 0
            for i in nodes:
                if i != mof_max_delta_m:
                    kmi = k_pairs[(mof_max_delta_m, i)]
                    lmi = l_pairs[(mof_max_delta_m, i)]
                    Xmi = node_pos[mof_max_delta_m][0] - node_pos[i][0]
                    Ymi = node_pos[mof_max_delta_m][1] - node_pos[i][1]
                    pw  =      np.power( Xmi * Xmi + Ymi * Ymi , 0.5)
                    dEdx[mof_max_delta_m] += kmi * ( Xmi - lmi * Xmi / pw )
                    dEdy[mof_max_delta_m] += kmi * ( Ymi - lmi * Ymi / pw )

            cur_delta_m = np.sqrt(dEdx[mof_max_delta_m] * dEdx[mof_max_delta_m] +
                                    dEdy[mof_max_delta_m] * dEdy[mof_max_delta_m])
            # print("cur[{0}] deltaM = {1}".format(mof_max_delta_m,cur_delta_m))
        
        posout.append(deepcopy(node_pos))

iterate()

fig = plt.figure()
fig.set_size_inches(5, 5)
plt.xlim(-1., 1.)
plt.ylim(-1., 1.)
plt.get_current_fig_manager().set_window_title("KK force-directed test")

def drawg(pos):
    plt.cla()
    nx.draw_networkx(
        G=g,
        pos=pos,
        node_size=80,
        node_shape="o",
        edge_color="#aaa",
        width=1.5,
        font_size=6,
        font_color="#fff",
    )


anim = ani.FuncAnimation(fig=fig,
                         func=drawg,
                         frames=posout,
                         interval=33,
                         repeat=False,)


# pos = nx.kamada_kawai_layout(g)
# nx.draw_networkx(
#         G=g,
#         pos=pos,
#         node_size=80,
#         node_shape="o",
#         edge_color="#aaa",
#         width=1.5,
#         font_size=6,
#         font_color="#fff",
#     )


# fig = plt.figure()
# fig.set_size_inches(5, 5)
# plt.xlim(-1., 1.)
# plt.ylim(-1., 1.)
# plt.get_current_fig_manager().set_window_title("FR force-directed test")


# pos = nx.fruchterman_reingold_layout(g)
# nx.draw_networkx(
#         G=g,
#         pos=pos,
#         node_size=80,
#         node_shape="o",
#         edge_color="#aaa",
#         width=1.5,
#         font_size=6,
#         font_color="#fff",
#     )


plt.show()

