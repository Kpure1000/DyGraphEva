import json
import networkx as nx

def dict2graph(dict):
    g = nx.Graph()
    for node in dict['nodes']:
        g.add_node(node['id'], group=node['group'])
    for edge in dict['links']:
        if 'weight' in edge:
            g.add_edge(edge['source'], edge['target'], weight=edge['weight'])
        else:
            g.add_edge(edge['source'], edge['target'], weight=1.0)
    return g


def read_graph(filename):
    with open(filename, 'r') as jsonIn:
        jsonStr = jsonIn.read()
        jsonIn.close()
    gJson = json.loads(jsonStr)
    g = dict2graph(gJson)
    return g


gs = []

for i in range(1, 6):
    # g = read_graph("../data/dataset/truth/newcomb/newcomb_{0}.json".format(i))
    g = read_graph("../data/dataset/synth/test0/test{0}.json".format(i))
    # g = read_graph("../data/dataset/synth/node_eva/node_eva_{0}.json".format(i))
    gs.append(g)

ccs = []

for g in gs:
    cc = nx.closeness_centrality(g, distance='weight')
    ccs.append(cc)

nodes_cc = []

node_ids = gs[0].nodes()

for node_id in node_ids:
    cc_delta = 0
    for i in range(0, ccs.__len__() - 1):
        if i + 1 != ccs.__len__():
            cc_delta += abs(ccs[i + 1][node_id] - ccs[i][node_id])
    nodes_cc.append({'id': node_id, 'cc': cc_delta})

nodes_cc.sort(key=lambda ele: ele['cc'], reverse=True)

for node_cc in nodes_cc:
    print(node_cc)