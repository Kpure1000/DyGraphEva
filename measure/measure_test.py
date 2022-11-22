import measurements as ms
import task_total as tt
import networkx as nx


def pair_nodes():


    G0 = nx.Graph()

    for i in range(1, 5):
        G0.add_edge(0, i, weight=1.0)
        G0.add_edge(5, i + 5, weight=1.0)

    G0.add_node(10)
    G0.add_node(11)
    G0.add_node(12)
    nx.set_node_attributes(G=G0, values=0, name='block')

    G0.add_edge(0,5,weight=0.1)

    gs=[]

    # gs.append(G0)

    # G1 = G0.copy()
    # G1.add_edge(0, 10, weight=1)
    # G1.add_edge(10, 5, weight=1)

    # nx.set_node_attributes(G=G1, values=0, name='block')
    # gs.append(G1)

    # # nx.draw_networkx(G=G1)
    # # import matplotlib.pyplot as plt
    # # plt.show()

    # G2 = G1.copy()
    # G2.add_edge(0, 11, weight=1)
    # G2.add_edge(11, 5, weight=1)
    # nx.set_node_attributes(G=G2, values=0, name='block')
    # gs.append(G2)


    # G3 = G2.copy()
    # G3.add_edge(0, 12, weight=1)
    # G3.add_edge(12, 5, weight=1)
    # nx.set_node_attributes(G=G3, values=0, name='block')
    # gs.append(G3)

    for i in range(0, 200):
        Gi = G0.copy()
        Gi[0][5]['weight']=0.05 + i * 0.05
        gs.append(Gi)

    return gs

gs = pair_nodes()


def sp_get(Gs, s, t):
    print("sp:")
    ml = [ms.ShortestPath(G).get(s, t) for G in Gs]
    print(ml)



def act_get(Gs, s, t):
    print("act:")
    ml = [ms.ACT(G).get(s, t) for G in Gs]
    print(ml)


def kz_get(Gs, s, t):
    print("kz:")
    ml = [ms.KatzIndex(G, b=1.099).get(s, t) for G in Gs]
    print(ml)

    return ml


def rwr_get(Gs, s, t):
    print("rwr:")
    ml = [ms.RWR(G, alpha=0.1).get(s, t) for G in Gs]
    print(ml)


# sp_get(gs, 3, 8)
# act_get(gs, 3, 8)
ml = kz_get(gs, 3, 8)
# rwr_get(gs, 3, 8)

import matplotlib.pyplot as plt
plt.get_current_fig_manager().set_window_title('Katz Index of [3, 8]')
plt.plot([0.05 + 0.05 * i for i in range(len(gs))], ml, '.-g')

plt.show()
