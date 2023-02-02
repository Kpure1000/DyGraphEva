import networkx as nx
import pandas as pd


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

    with open("../../data/dataset/truth/wildbird/wildbird_{0}.json".format(days),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()


data = pd.read_csv("../../data/dataset/truth/wildbird/aves-wildbird-network.edges", sep=' ')
ar = data.to_numpy()

Days = {}

for row in ar:
    day = row[3]
    if day not in Days:
        Days[day] = {'g': nx.Graph(), 's': set()}
    Days[day]['g'].add_edge(row[0], row[1], weight=row[2])
    Days[day]['s'].add(row[0])
    Days[day]['s'].add(row[1])


node_inter_set = Days[list(Days)[0]]['s']
node_union_set = Days[list(Days)[0]]['s']
for d in Days:
    print(len(Days[d]['s']))
    node_inter_set = node_inter_set & Days[d]['s']
    node_union_set = node_union_set | Days[d]['s']

for d in Days:
    G = Days[d]['g']
    G.remove_edges_from(list(nx.selfloop_edges(G)))
    # G.remove_nodes_from(set(G.nodes) - node_inter_set)
    # G.add_nodes_from(node_union_set - set(G.nodes))

# cluster 0 [151,122,118,107,124,120,116,112,111,109,67,119,113,70,123,117,114,108,110,68,115,129,121,195,186,197,69,52,66]



# nx.draw_networkx(Days[list(Days)[1]]['g'])
# import matplotlib.pyplot as plt
# plt.show()

for i, d in enumerate( Days ):
    save_graph(Days[d]['g'], i)
