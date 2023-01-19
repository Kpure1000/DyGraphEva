import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import json


def intra_add(g, cl_nodes, min=0.0, max=0.0, weight='weight'):
    l_cl_nodes = list(cl_nodes)
    for s in range(len(l_cl_nodes)):
        for t in range(s):
            if g.has_edge(l_cl_nodes[s],l_cl_nodes[t]):
                g[l_cl_nodes[s]][l_cl_nodes[t]][weight] += np.random.uniform(min,max)


def intra_multi(g, cl_nodes, min=1.0, max=1.0, weight='weight'):
    l_cl_nodes = list(cl_nodes)
    for s in range(len(l_cl_nodes)):
        for t in range(s):
            if g.has_edge(l_cl_nodes[s],l_cl_nodes[t]):
                g[l_cl_nodes[s]][l_cl_nodes[t]][weight] *= np.random.uniform(min,max)


def intra_cluster():
    c1, c2, c3, c4, c5= 40, 40, 40, 40, 40
    sizes = [c1, c2, c3, c4, c5]
    intra_prob = 0.55
    inter_prob = 0.025
    probs = [
        [intra_prob, inter_prob, inter_prob, inter_prob, inter_prob],
        [inter_prob, intra_prob, inter_prob, inter_prob, inter_prob],
        [inter_prob, inter_prob, intra_prob, inter_prob, inter_prob],
        [inter_prob, inter_prob, inter_prob, intra_prob, inter_prob],
        [inter_prob, inter_prob, inter_prob, inter_prob, intra_prob],
    ]
    G = nx.stochastic_block_model(sizes, probs, seed=0)

    nx.set_edge_attributes(G, 10.0, 'weight')

    np.random.seed(0)

    old_size = sum(sizes)
    adding_node = 20
    for i in range(adding_node):
        G.add_node(i + old_size, block=5)
    new_size = old_size + adding_node
    for i in range(adding_node):
        edges_num = int(np.random.uniform(3, 10))
        for e in range(edges_num):
            other = int(np.random.uniform(0, new_size))
            if other == i + old_size: continue
            G.add_edge(i + old_size,
                       other,
                       weight=np.random.uniform(20.0, 80.0))


    c1_nodes = {n: G.nodes[n] for n in G.nodes if G.nodes[n]['block'] == 0}
    c2_nodes = {n: G.nodes[n] for n in G.nodes if G.nodes[n]['block'] == 1}
    c3_nodes = {n: G.nodes[n] for n in G.nodes if G.nodes[n]['block'] == 2}
    c4_nodes = {n: G.nodes[n] for n in G.nodes if G.nodes[n]['block'] == 3}
    c5_nodes = {n: G.nodes[n] for n in G.nodes if G.nodes[n]['block'] == 4}

    G0 = G.copy()

    G1 = G0.copy()
    intra_multi(G1, c1_nodes, 1.0, 2.0)
    intra_multi(G1, c2_nodes, 1.0, 4.0)
    intra_multi(G1, c3_nodes, 0.5, 1.0)
    # intra_add(G1, c4_nodes, 0.0, 40.0)
    # intra_add(G1, c5_nodes, 20.0,40.0)

    G2 = G1.copy()

    intra_multi(G2, c1_nodes, 1.0, 2.0)
    intra_multi(G2, c2_nodes, 1.0, 4.0)
    intra_multi(G2, c3_nodes, 0.5, 1.0)
    # intra_add(G2, c4_nodes, 0.0, 40.0)
    # intra_add(G2, c5_nodes, -0.0,0.0)

    G3 = G2.copy()
    intra_multi(G3, c1_nodes, 1.0, 2.0)
    intra_multi(G3, c2_nodes, 0.2, 1.0)
    intra_multi(G3, c3_nodes, 0.5, 1.0)
    # intra_add(G3, c4_nodes, 0.0, 0.0)
    # intra_add(G3, c5_nodes, 20.0,40.0)

    G4 = G3.copy()
    intra_multi(G4, c1_nodes, 1.0, 2.0)
    intra_multi(G4, c2_nodes, 0.2, 1.0)
    intra_multi(G4, c3_nodes, 0.5, 1.0)
    # intra_add(G4, c4_nodes, 0.0, 20.0)
    # intra_add(G4, c5_nodes, -20.0,0.0)

    gs = [G0, G1, G2, G3, G4]

    for g in gs:
        for edge in g.edges:
            g[edge[0]][edge[1]]['capacity'] = 1.0 / g[edge[0]][edge[1]]['weight']

    return gs

def save_graph(g, days):

    g_json = {
        'nodes': [],
        'links': [],
    }

    nodes = dict(g.nodes)

    for node in nodes:
        # print(node)
        g_json["nodes"].append({"id": node, "group": nodes[node]['block']})

    for edge in g.edges(data=True):
        g_json["links"].append({
            "source": edge[0],
            "target": edge[1],
            "weight": edge[2]["weight"],
        })

    with open("../data/dataset/synth/intra_cluster/intra_cluster_{0}.json".format(days),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()

gs = intra_cluster()

for g in gs:
    save_graph(g,gs.index(g) + 1)
