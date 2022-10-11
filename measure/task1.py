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


def read_SingleGraph(filename):
    with open(filename, 'r') as jsonIn:
        jsonStr = jsonIn.read()
        jsonIn.close()
    gJson = json.loads(jsonStr)
    g = dict2graph(gJson)
    return g


def closeness_centrality(gs):
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

    return nodes_cc


def mean_first_pass_time(gs):
    nodes_mfpt=[]
    return nodes_mfpt


def read_Graphs(path, name):
    gs = []
    # read config
    with open("{0}{1}.json".format(path, name)) as jsonIn:
        config = json.loads(jsonIn.read())
        jsonIn.close()

    for i in range(1, config['days'] + 1):
        g = read_SingleGraph("{0}{1}{2}.json".format(path, config['prefix'], i))
        gs.append(g)

    return gs


gs = read_Graphs("../data/dataset/synth/test0/", "test")
# gs = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
# gs = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")


nodes_cc = closeness_centrality(gs)
print("Node Closeness Centrality (descend): ")
for node_cc in nodes_cc:
    print("Node '{0}':\t{1:.4f}".format(node_cc['id'],node_cc['cc']))
