import measurements as ms
import task_total as tt
import networkx as nx


def pair_nodes():

    #        C1  C2  C3
    sizes = [10, 10, 10]

    p = [
        [0.6, 0.0, 0.0],
        [0.0, 0.6, 0.0],
        [0.0, 0.0, 0.6],
    ]

    G0 = nx.stochastic_block_model(sizes, p, seed=0)

    nx.set_edge_attributes(G0, 1, 'weight')

    # nx.draw_networkx(G=G0)

    # plt.show()

    gs=[]

    G0.add_edge(0, 20, weight=1.0)
    gs.append(G0)

    G1 = G0.copy()
    G1.add_edge(3, 13, weight=1)
    G1.add_edge(13, 23, weight=1)
    G1.add_edge(4, 14, weight=1)
    G1.add_edge(14, 24, weight=1)
    gs.append(G1)

    G2 = G1.copy()
    G2.add_edge(5, 15, weight=1)
    G2.add_edge(16, 26, weight=1)
    G2.add_edge(7, 17, weight=1)
    G2.add_edge(18, 28, weight=1)
    gs.append(G2)
    

    G3 = G2.copy()
    G3[0][20]['weight']=8.0
    gs.append(G3)

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
    ml = [ms.KatzIndex(G, b=0.099).get(s, t) for G in Gs]
    print(ml)


def rwr_get(Gs, s, t):
    print("rwr:")
    ml = [ms.RWR(G, alpha=0.1).get(s, t) for G in Gs]
    print(ml)


sp_get(gs, 9, 29)
act_get(gs, 9, 29)
kz_get(gs, 9, 29)
rwr_get(gs, 9, 29)
