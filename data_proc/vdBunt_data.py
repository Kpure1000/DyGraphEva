import json
import networkx as nx
import numpy as np


def mat2graph(filename):
    with open(filename, 'r') as f:
        l = [[int(num) for num in line.split(' ') if num != ''] for line in f]

    G = nx.Graph()

    for row in range(0, len(l)):
        for col in range(0, len(l[row])):
            if (row != col and l[row][col] != 0 and l[row][col] != 9 and l[row][col] != 6):
                edge = (row, col)
                weight = l[row][col]
                # print({edge: {'weight': weight}})
                G.add_edge(edge[0], edge[1], weight=weight)
                G.add_node(row, group=0)
                G.add_node(col, group=0)

    return G


def graph2dict(g):
    node_dict = dict(g.nodes)
    edge_dict = dict(g.edges)

    dictOut={}
    dictOut['nodes']=[]
    for node in node_dict:
        dictOut['nodes'].append({
            'id': node,
            'group': node_dict[node]['group']
        })

    dictOut['links']=[]
    for edge in edge_dict:
        # if edge_dict[edge]['weight'] != 9 and edge_dict[edge]['weight'] != 6:
        dictOut['links'].append({
            'source': edge[0],
            'target': edge[1],
            'weight': edge_dict[edge]['weight']
        })

    return dictOut

gs=[]

for i in range(0, 7):
    # fin = "../data/dataset/truth/vdBunt_data/FR{0}.DAT".format(i)
    fin = "../data/dataset/truth/vdBunt_data/VRND32T{0}.DAT".format(i)
    gs.append(mat2graph(fin))

all_nodes={}
for g in gs:
    nodes = dict(g.nodes)
    for node in nodes:
        all_nodes[node]=nodes[node]

for g in gs:
    g.add_nodes_from(all_nodes, group=0)
    print(g)

for i in range(0, 7):
    # fout = "../data/dataset/truth/vdBunt_data/FR{0}.json".format(i)
    fout = "../data/dataset/truth/vdBunt_data/VRND32T{0}.json".format(i)
    with open(fout, 'w') as f:
        f.write(json.dumps(graph2dict(gs[i])))
        f.flush()
        f.close()
