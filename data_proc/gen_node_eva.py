import json
import networkx as nx

count = 1

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

    with open("../data/dataset/synth/node_eva/node_eva_{0}.json".format(days),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()


def gen_graph(sizes, probs):
    global count

    g = nx.stochastic_block_model(sizes, probs, seed=0)
    save_graph(g, count)
    count += 1

def old():
    sizes = [5, 6, 7]
    probs = [
        [0.75, 0.01, 0.01],
        [0.01, 0.75, 0.01],
        [0.01, 0.01, 0.85],
    ]
    gen_graph(sizes, probs)

    probs = [
        [0.75, 0.06, 0.01],
        [0.06, 0.75, 0.01],
        [0.01, 0.01, 0.85],
    ]
    gen_graph(sizes, probs)

    probs = [
        [0.75, 0.11, 0.01],
        [0.11, 0.75, 0.01],
        [0.01, 0.01, 0.85],
    ]
    gen_graph(sizes, probs)

    probs = [
        [0.75, 0.16, 0.01],
        [0.16, 0.75, 0.01],
        [0.01, 0.01, 0.85],
    ]
    gen_graph(sizes, probs)

    probs = [
        [0.75, 0.21, 0.01],
        [0.21, 0.75, 0.01],
        [0.01, 0.01, 0.85],
    ]
    gen_graph(sizes, probs)


# old()

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8], group=0)
G.add_edges_from([(1, 4), (2, 4), (3, 4), (4, 5), (5, 6), (5, 7), (5, 8)], weight=1)

save_graph(G, 6)

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8], group=0)
G.add_edges_from([(1, 5), (2, 5), (3, 5), (4, 5), (4, 6), (4, 7), (4, 8)], weight=1)

save_graph(G, 7)

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8], group=0)
G.add_edges_from([(1, 4), (2, 4), (3, 4), (4, 5), (5, 6), (5, 7), (5, 8)], weight=1)

save_graph(G, 8)
