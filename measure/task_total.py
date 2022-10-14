import networkx as nx
import json

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

# sum of value delta
def delta_sum(gs_metrics):
    keys_delta=[]
    for key in gs_metrics[0]:
        delta_val=0
        for i in range(0, gs_metrics.__len__()-1):
            if i+1!=gs_metrics.__len__():
                delta_val += abs( gs_metrics[i+1][key] - gs_metrics[i][key] )
        keys_delta.append({"id":key,"val":delta_val})
    return keys_delta
