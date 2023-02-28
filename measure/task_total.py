import networkx as nx
import json

def dict2graph(dictIn):
    g = nx.Graph()
    for node in dictIn['nodes']:
        g.add_node(node['id'], group=node['group'])
    for edge in dictIn['links']:
        g.add_edge(edge['source'], edge['target'])
        if 'weight' in edge:
            nx.set_edge_attributes(g,{(edge['source'], edge['target']):{'weight':edge['weight']}})
        else:
            nx.set_edge_attributes(g,{(edge['source'], edge['target']):{'weight':1.0}})
        if 'capacity' in edge:
            nx.set_edge_attributes(g,{(edge['source'], edge['target']):{'capacity':edge['capacity']}})
        else:
            nx.set_edge_attributes(g,{(edge['source'], edge['target']):{'capacity':1.0}})
    return g


def read_SingleGraph(filename):
    with open(filename, 'r') as jsonIn:
        jsonStr = jsonIn.read()
        jsonIn.close()
    gJson = json.loads(jsonStr)
    g = dict2graph(gJson)
    return g


def read_Graphs(path, name):
    gs = []
    # read config
    with open("{0}{1}.json".format(path, name)) as jsonIn:
        config = json.loads(jsonIn.read())
        jsonIn.close()

    for i in range(config['day_start'], config['day_end'] + 1):
        g = read_SingleGraph("{0}{1}{2}.json".format(path, config['prefix'], i))
        gs.append(g)

    return gs


def print_l(pairs_delta_list, method_name, print_lim):
    print("[{0}] Variation:".format(method_name))
    for i, pair_res in enumerate(pairs_delta_list):
        if i < print_lim:
            print("Pair '{0}':\t{1:.4f}".format(pair_res['id'],pair_res['val']))


def weight2length(gs):
    for g in gs:
        w = nx.get_edge_attributes(g, 'weight')
        inv_w = {pair: 1.0 / (w[pair] + 1e-5) for pair in w}
        nx.set_edge_attributes(g, inv_w, 'length')

    return gs
