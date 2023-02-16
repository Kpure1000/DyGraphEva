import networkx as nx
import pandas as pd
import numpy as np

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
            "group": nodes[node]['group'],
        })

    for edge in g.edges(data=True):
        g_json["links"].append({
            "source": edge[0],
            "target": edge[1],
            "weight": edge[2]["weight"],
        })

    with open(f'../../data/dataset/truth/reality_mining/reality_mining_{days}.json','w') as file:
        file.write( json.dumps(g_json) )
        file.close()


def remove_loop(Sec):
    for s in Sec:
        G = Sec[s]['g']
        G.remove_edges_from(list(nx.selfloop_edges(G)))


def remove_diff(Sec, start, end):
    node_set = Sec[list(Sec)[start]]['s']
    for i, s in enumerate(Sec):
        if i >= start and i <= end:
            node_set = node_set & Sec[s]['s']
    for i, s in enumerate(Sec):
        if i >= start and i <= end:
            G = Sec[s]['g']
            G.remove_nodes_from(set(G.nodes) - node_set)


def remove_nodes(Sec, nodes_list):
    for s in Sec:
        Sec[s]['g'].remove_nodes_from(nodes_list)


def save_image(Sec):
    import matplotlib.pyplot as plt
    # pos = None
    for i, s in enumerate(Sec):
        fig = plt.figure()
        G = Sec[s]['g']
        # pos = nx.fruchterman_reingold_layout(G, pos)
        nx.draw_networkx(G,
                        #  pos=pos,
                        with_labels=False,
                        node_size=20,
                        node_color='gray',
                        linewidths=0.2)
        plt.axis("off")
        fig.savefig(f'imgout_reality_mining/{i}_{len(G)}.jpg')
        plt.close(fig)


# src, tar, w, ti
data = pd.read_csv("../../data/dataset/truth/reality_mining/edges.csv",sep=',')
ar = data.to_numpy()
arl = list(ar)
arl.sort(key=lambda el:el[3])
ar = np.array( arl )

time = ar[0][0]
g_count = 0
Sec = {}
n_count = 0
Nodes = {}
# c_count = 0
# Cluster = {}

internal = 60 * 60 * 24 * 4
window = 60 * 60 * 24 * 7
slide_time = ar[0][3]
is_window = True
for i in range(len(ar)):
    # if ar[i][3] > 62300:
    #     break

    if ar[i][3] - slide_time >= internal:  # slide
        is_window = True
        slide_time = ar[i][3]
        g_count += 1

    if is_window is True:
        is_window = False
        window_time = ar[i][3]
        Sec[g_count] = {'g': nx.Graph(), 's': set()}
        for j in range(i, len(ar)):
            row = ar[j]
            sec = row[3]
            # if sec > 62300:
            #     print("buzu")
            #     break

            if sec - window_time >= window:
                break

            if row[0] not in Nodes:
                Nodes[row[0]] = n_count
                n_count += 1
            if row[1] not in Nodes:
                Nodes[row[1]] = n_count
                n_count += 1

            # if row[3] not in Cluster:
            #     Cluster[row[3]] = c_count
            #     c_count += 1

            # if row[4] not in Cluster:
            #     Cluster[row[4]] = c_count
            #     c_count += 1

            Sec[g_count]['g'].add_nodes_from([
                ( Nodes[row[0]], {'group': 0} ),
                ( Nodes[row[1]], {'group': 0} ),
            ])

            if Sec[g_count]['g'].has_edge(Nodes[row[0]], Nodes[row[1]]):
                Sec[g_count]['g'][Nodes[row[0]]][Nodes[row[1]]]['weight'] += float(row[2])
            else:
                Sec[g_count]['g'].add_edge(Nodes[row[0]], Nodes[row[1]], weight=float(row[2]))

            Sec[g_count]['s'].add(Nodes[row[0]])
            Sec[g_count]['s'].add(Nodes[row[1]])

print(len(Sec))
remove_loop(Sec)
remove_diff(Sec, 52, 56)
remove_nodes(Sec, [4, 0])
# save_image(Sec)

for i, s in enumerate( Sec ):
    save_graph(Sec[s]['g'], i)
