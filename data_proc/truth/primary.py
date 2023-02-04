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


# G0 = nx.read_gexf('../../data/dataset/truth/primary/sp_data_school_day_1_g.gexf')
# G1 = nx.read_gexf('../../data/dataset/truth/primary/sp_data_school_day_2_g.gexf')

# nx.draw_networkx(G1)
# import matplotlib.pyplot as plt
# plt.show()

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
for row in ar:
    sec = row[0]
    if sec - time >= 60 * 60 * 5.3: # 3.1
        time = sec
        g_count += 1
    if g_count not in Sec:
        # print(f'days:{g_count}, sec:{sec}')
        Sec[g_count] = {'g': nx.Graph(), 's': set()}

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

node_set = Sec[list(Sec)[0]]['s']
for y in Sec:
    node_set = node_set & Sec[y]['s']

for y in Sec:
    G = Sec[y]['g']
    G.remove_edges_from(list(nx.selfloop_edges(G)))
    # G.remove_nodes_from(set(G.nodes) - node_set)

# Sec[list(Sec)[2]]['g'].add_edges_from([(85, 43), (54, 25), (53, 188),
#                                        (107, 181)],
#                                       weight=1.0)


# import matplotlib.pyplot as plt
# # pos = None
# for i, s in enumerate(Sec):
#     fig = plt.figure()
#     G = Sec[s]['g']
#     # pos = nx.fruchterman_reingold_layout(G, pos)
#     nx.draw_networkx(G,
#                     #  pos=pos,
#                      with_labels=False,
#                      node_size=20,
#                      node_color='gray',
#                      linewidths=0.2)
#     plt.axis("off")
#     fig.savefig(f'primaryout/{i}_{len(G)}.jpg')
#     plt.close(fig)

for i, s in enumerate( Sec ):
    save_graph(Sec[s]['g'], i)

# gout = 0
# for i, s in enumerate( Sec ):
#     if i == 0 or i == 2 or i == 3 or i == 5:
#         save_graph(Sec[s]['g'], gout)
#         gout += 1
