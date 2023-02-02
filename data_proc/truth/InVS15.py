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

    with open("../../data/dataset/truth/InVS15/InVS15_{0}.json".format(days),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()


data = pd.read_csv("../../data/dataset/truth/InVS15/copresence-InVS15.edges", sep=' ')
ar = data.to_numpy()

time = ar[0][2]
g_count = 1
Sec = {}
for row in ar:
    if row[2] - time >= 60 * 60 * 24:
        time = row[2]
        g_count += 1
    if g_count not in Sec:
        print(f'days:{g_count}, sec:{row[2]}')
        Sec[g_count] = {'g': nx.Graph(), 's': set()}
    Sec[g_count]['g'].add_edge(int(row[0]), int(row[1]), weight=1.0)
    Sec[g_count]['s'].add(row[0])
    Sec[g_count]['s'].add(row[1])

print(len(Sec))

# nx.draw_networkx(Sec[list(Sec)[9]]['g'])
# import matplotlib.pyplot as plt
# plt.show()

for i, s in enumerate( Sec ):
    save_graph(Sec[s]['g'], i)
