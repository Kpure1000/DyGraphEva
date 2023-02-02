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

    with open("../../data/dataset/truth/tortoise/tortoise_{0}.json".format(days),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()


data = pd.read_csv("../../data/dataset/truth/tortoise/reptilia-tortoise-network-bsv.edges", sep=' ')
ar = data.to_numpy()

time = ar[0][2]
Years = {}
for row in ar:
    years = row[2]
    if years not in Years:
        Years[years] = {'g': nx.Graph(), 's': set()}
    Years[years]['g'].add_edge(int(row[0]), int(row[1]), weight=1.0)
    Years[years]['s'].add(row[0])
    Years[years]['s'].add(row[1])

print(len(Years))

# nx.draw_networkx(Years[list(Years)[2]]['g'])
# import matplotlib.pyplot as plt
# plt.show()

for i, s in enumerate( Years ):
    save_graph(Years[s]['g'], i)
