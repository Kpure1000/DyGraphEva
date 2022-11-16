import networkx as nx
import json

def cluster_gen():
    n1, n2, n3, n4, n5, n6 = 30, 30, 30, 30, 30, 30
    sizes1 = [n1, n2, n3, n4, n5, n6]
    probs1 = [[0.2, 0.00, 0.00, 0.00, 0.00, 0.00],
              [0.00, 0.2, 0.00, 0.00, 0.00, 0.00],
              [0.00, 0.00, 0.2, 0.00, 0.00, 0.00],
              [0.00, 0.00, 0.00, 0.2, 0.00, 0.00],
              [0.00, 0.00, 0.00, 0.00, 0.25, 0.00],
              [0.00, 0.00, 0.00, 0.00, 0.00, 0.25]]
    G = nx.stochastic_block_model(sizes1, probs1, seed=0)
    edges = G.edges()
    for i, j in edges:
        G[i][j]['capacity'], G[i][j]['weight'] = 1, 1
    G.add_edge(0, 16, weight=1/2, capacity=2)
    G.add_edge(0, 20, weight=1/2, capacity=2)
    common_num = 18
    common_edge12, common_edge34 = [], []
    edge5, edge6 = [], []
    for i in range(0, common_num):
        G.add_edge(i, i + n1, weight=1, capacity=1)
        common_edge12.append([i, i + n1])
        G.add_edge(i + n1 + n2, i + n1 + n2 + n3, weight=1, capacity=1)
        common_edge34.append([i + n1 + n2, i + n1 + n2 + n3])
    n, m = G.number_of_nodes(), G.number_of_edges()

    for i, j in G.edges():
        u5, v5 = n1 + n2 + n3 + n4, n1 + n2 + n3 + n4 + n5
        u6, v6 = n1 + n2 + n3 + n4 + n5, n1 + n2 + n3 + n4 + n5 + n6
        if u5 <= i < v5 and u5 <= j < v5:
            edge5.append([i, j])
        if u6 <= i < v6 and u6 <= j < v6:
            edge6.append([i, j])

    G.add_node(n, block=-1)
    G.add_node(n + 1, block=-1)
    G.add_edge(n, n + 1, weight=1/1.5, capacity=1.5)
    # nx.set_node_attributes(G, {n + 1: -1}, "group")

    graph_list = []
    # capacity_list12 = [0.05, 0.1, 0.2, 0.4, 0.8, 1.2, 1.8, 2.4, 3, 5]
    # capacity_list12 = [0.25, 0.5, 1, 2, 3]
    capacity_list12 = [0.2, 0.5, 1, 2, 3.5]
    capacity_list34 = capacity_list12.copy()
    capacity_list34.reverse()
    # capacity_list5 = [1, 1.3, 1.6, 1.9, 2.4, 2.8, 3.2, 3.6, 4, 4.5]
    # capacity_list5 = [1, 1.5, 2, 2.5, 3]
    capacity_list5 = [1, 1.3, 1.6, 1.9, 2.4]
    capacity_list6 = capacity_list5.copy()
    capacity_list6.reverse()

    for i in range(len(capacity_list12)):
        Gc = G.copy()
        for u, v in common_edge12:
            Gc[u][v]['capacity'] = capacity_list12[i]
            Gc[u][v]['weight'] = 1 / capacity_list12[i]
        for u, v in common_edge34:
            Gc[u][v]['capacity'] = capacity_list34[i]
            Gc[u][v]['weight'] = 1 / capacity_list34[i]
        for u, v in edge5:
            Gc[u][v]['capacity'] = capacity_list5[i]
            Gc[u][v]['weight'] = 1 / capacity_list5[i]
        for u, v in edge6:
            Gc[u][v]['capacity'] = capacity_list6[i]
            Gc[u][v]['weight'] = 1 / capacity_list6[i]
        graph_list.append(Gc)

    return graph_list


def save_graph(g, days):

    g_json = {
        'nodes': [],
        'links': [],
    }

    nodes = dict(g.nodes)

    for node in nodes:
        # print(node)
        g_json["nodes"].append({"id": node, "group": nodes[node]['block']})

    for edge in g.edges(data=True):
        g_json["links"].append({
            "source": edge[0],
            "target": edge[1],
            "weight": edge[2]["weight"],
            "capacity": edge[2]["capacity"],
        })

    with open("../data/dataset/synth/cluster/cluster_{0}.json".format(days),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()

gs = cluster_gen()

for g in gs:
    save_graph(g,gs.index(g) + 1)

