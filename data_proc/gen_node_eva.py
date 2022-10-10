import json
import networkx as nx

count = 1

def gen_graph(sizes, probs):
    global count

    g = nx.stochastic_block_model(sizes, probs, seed=0)

    g_json = {
        'nodes': [],
        'links': [],
    }

    for node in g.nodes(data='block'):
        g_json["nodes"].append({"id": node[0], "group": node[1]})

    for link in g.edges(data=True):
        g_json["links"].append({"source": link[0], "target": link[1]})

    with open("../data/dataset/synth/node_eva/node_eva_{0}.json".format(count),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()

    count += 1


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

sizes = [5, 5, 7]
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

sizes = [5, 4, 7]
probs = [
    [0.75, 0.21, 0.01],
    [0.21, 0.75, 0.01],
    [0.01, 0.01, 0.85],
]
gen_graph(sizes, probs)
