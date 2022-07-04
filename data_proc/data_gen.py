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

    with open("../data/dataset/synth/test{0}.json".format(count),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()

    count += 1


sizes = [12, 19, 18]
probs = [
    [0.55, 0.02, 0.01],
    [0.02, 0.65, 0.02],
    [0.01, 0.02, 0.45],
]
gen_graph(sizes, probs)

probs = [
    [0.65, 0.02, 0.01],
    [0.02, 0.55, 0.02],
    [0.01, 0.02, 0.35],
]
gen_graph(sizes, probs)

probs = [
    [0.55, 0.02, 0.01],
    [0.02, 0.45, 0.02],
    [0.01, 0.02, 0.25],
]
gen_graph(sizes, probs)

probs = [
    [0.45, 0.02, 0.02],
    [0.02, 0.35, 0.02],
    [0.02, 0.02, 0.05],
]
gen_graph(sizes, probs)

probs = [
    [0.35, 0.02, 0.05],
    [0.02, 0.35, 0.02],
    [0.05, 0.02, 0.15],
]
gen_graph(sizes, probs)
