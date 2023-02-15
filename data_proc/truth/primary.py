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
            "group": nodes[node]['group'],
        })

    for edge in g.edges(data=True):
        g_json["links"].append({
            "source": edge[0],
            "target": edge[1],
            "weight": edge[2]["weight"],
        })

    with open("../../data/dataset/truth/primary/primary_{0}.json".format(days),'w') as file:
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
        fig.savefig(f'imgout_primary/{i}_{len(G)}.jpg')
        plt.close(fig)


# 31220 1558	1567	3B	3B
data = pd.read_csv("../../data/dataset/truth/primary/primaryschool.csv", sep='\t')
ar = data.to_numpy()

time = ar[0][0]
g_count = 0
Sec = {}
n_count = 0
Nodes = {}
c_count = 0
Cluster = {}

internal = 60 * 6   # 6 mins
window = 60 * 60 * 1.2     # 60 mins
slide_time = ar[0][0]
is_window = True
for i in range(len(ar)):
    if ar[i][0] > 62300:
        break

    if ar[i][0] - slide_time >= internal:  # slide
        is_window = True
        slide_time = ar[i][0]
        g_count += 1

    if is_window is True:
        is_window = False
        window_time = ar[i][0]
        Sec[g_count] = {'g': nx.Graph(), 's': set()}
        for j in range(i, len(ar)):
            row = ar[j]
            sec = row[0]
            if sec > 62300:
                print("buzu")
                break

            if sec - window_time >= window:
                break

            if row[1] not in Nodes:
                Nodes[row[1]] = n_count
                n_count += 1
            if row[2] not in Nodes:
                Nodes[row[2]] = n_count
                n_count += 1

            if row[3] not in Cluster:
                Cluster[row[3]] = c_count
                c_count += 1

            if row[4] not in Cluster:
                Cluster[row[4]] = c_count
                c_count += 1

            Sec[g_count]['g'].add_nodes_from([
                ( Nodes[row[1]], {'group': Cluster[row[3]]} ),
                ( Nodes[row[2]], {'group': Cluster[row[4]]} ),
            ])

            if Sec[g_count]['g'].has_edge(Nodes[row[1]], Nodes[row[2]]):
                Sec[g_count]['g'][Nodes[row[1]]][Nodes[row[2]]]['weight'] += 1.0
            else:
                Sec[g_count]['g'].add_edge(Nodes[row[1]], Nodes[row[2]], weight=1.0)

            Sec[g_count]['s'].add(Nodes[row[1]])
            Sec[g_count]['s'].add(Nodes[row[2]])

print(len(Sec))
remove_loop(Sec)
remove_diff(Sec, 9, 15)
# save_image(Sec)

for i, s in enumerate( Sec ):
    save_graph(Sec[s]['g'], i)
