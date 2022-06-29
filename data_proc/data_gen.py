import json
import imp
import networkx as nx

sizes = [5, 8, 11]
#   a b c
# a * * *
# b * * *
# c * * *

probs = [
    [0.15, 0.09, 0.02],
    [0.09, 0.25, 0.07],
    [0.02, 0.07, 0.10],
]

g = nx.stochastic_block_model(sizes, probs, seed=0)

print("len: {0}".format(len(g)))

H = nx.quotient_graph(g, g.graph["partition"], relabel=True)

for v in H.nodes(data=True):
    print(round(v[1]["density"], 3))

for v in H.edges(data=True):
    print(round(1.0 * v[2]["weight"] / (sizes[v[0]] * sizes[v[1]]), 3))


g_json = {
    'nodes': [],
    'links': [],
}

for node in g.nodes(data='block'):
    g_json["nodes"].append({"id": node[0], "group": node[1]})

for link in g.edges(data=True):
    g_json["links"].append({"source": link[0], "target": link[1]})


with open("../data/dataset/synth/test.json",'w') as file:
    file.write( json.dumps(g_json) )
