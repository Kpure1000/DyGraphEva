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

    with open("../../data/dataset/truth/canVote/canVote_{0}.json".format(days),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()


data = pd.read_csv("../../data/dataset/truth/canVote/canVote_edgelist.txt")
ar = data.to_numpy()

Years = {}

for row in ar:
    if row[0] not in Years:
        Years[row[0]] = {'g': nx.Graph(), 's': set()}
    Years[row[0]]['g'].add_edge(row[1], row[2], weight=row[3])
    Years[row[0]]['s'].add(row[1])
    Years[row[0]]['s'].add(row[2])

node_set = Years[list(Years)[0]]['s']
for y in Years:
    node_set = node_set & Years[y]['s']

for y in Years:
    G = Years[y]['g']
    G.remove_edges_from(list(nx.selfloop_edges(G)))
    G.remove_nodes_from(set(G.nodes) - node_set)
    G.remove_nodes_from(["maxime-bernier","david-tilson","nathan-cullen"])
    G.remove_nodes_from(
        set(G.nodes) - {
            # "rob-nicholson", "carolyn-bennett", "mark-eyking", "john-mckay",
            # "tony-clement", "cheryl-gallant", "dean-allison", "tom-lukiwski",
            # "david-sweet"
            "rob-nicholson",
            "tony-clement",
            "cheryl-gallant",
            "dean-allison",
            "tom-lukiwski",
            "david-sweet",
            "john-mckay",
            "mark-eyking",
            "carolyn-bennett",
            "judy-sgro",
            "rodger-cuzner",
            "scott-brison",
            "lawrence-macaulay",
            "brian-masse",
            "larry-miller",
            "harold-albrecht",
            "bev-shipley",
            "bradley-trost",
            "ralph-goodale",
            "dominic-leblanc",
            "michael-chong",
            "pierre-poilievre",
            "dave-mackenzie",
            "blaine-calkins",
            "ed-fast"
        })



for i, y in enumerate(Years):
    save_graph(Years[y]["g"], i)
