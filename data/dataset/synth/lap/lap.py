import networkx as nx
import json

def save_graph(g, days):
    import json
    g_json = {
        'nodes': [],
        'links': [],
    }

    nodes = dict(g.nodes)

    for node in nodes:
        g_json["nodes"].append({
            "id": node,
            "group": 0,
        })

    for edge in g.edges(data=True):
        g_json["links"].append({
            "source": edge[0],
            "target": edge[1],
            "weight": edge[2]["weight"],
        })

    with open("lap_{0}.json".format(days),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()


G0 = nx.Graph([(0, 1), (1, 2), (3, 0), (2, 3)])

G1 = nx.Graph([(0, 1), (1, 2), (3, 0), (3, 7), (7, 6), (6, 5), (5, 4), (4, 2)])
nx.set_edge_attributes(G0, 1.0, 'weight')
nx.set_edge_attributes(G1, 1.0, 'weight')

save_graph(G0, 1)
save_graph(G1, 2)
