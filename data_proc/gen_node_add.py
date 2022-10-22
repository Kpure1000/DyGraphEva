import json
import networkx as nx

def save_graph(g, days):

    g_json = {
        'nodes': [],
        'links': [],
    }

    for node in g.nodes(data='group'):
        g_json["nodes"].append({"id": node[0], "group": node[1]})

    for link in g.edges(data=True):
        g_json["links"].append({
            "source": link[0],
            "target": link[1],
            "weight": link[2]["weight"]
        })

    with open("../data/dataset/synth/node_add/node_add_{0}.json".format(days),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4], group=0)
G.add_edges_from([(1, 2), (2, 3)], weight=1)

save_graph(G, 1)

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5], group=0)
G.add_edges_from([(1, 2), (2, 3), (2, 4), (1, 5)], weight=1)

save_graph(G, 2)

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7], group=0)
G.add_edges_from([(1, 2), (2, 3), (2, 4), (1, 5), (6, 7), (1, 6)], weight=1)

save_graph(G, 3)

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8], group=0)
G.add_edges_from([(1, 2), (2, 4), (1, 5), (6, 7), (1, 6), (7, 8), (4, 8), (5, 8)], weight=1)

save_graph(G, 4)
