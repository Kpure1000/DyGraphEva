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
        distance_scale=1
        if 'distance_scale' in config:
            distance_scale =  config['distance_scale']
    return gs, distance_scale


def graph2dict(g):
    node_dict = dict(g.nodes)
    edge_dict = dict(g.edges)

    dictOut={}
    dictOut['nodes']=[]
    for node in node_dict:
        dictOut['nodes'].append({
            'id': node,
            'x': node_dict[node]['pos'][0],
            'y': node_dict[node]['pos'][1],
            'group': node_dict[node]['group']
        })
    
    dictOut['links']=[]
    for edge in edge_dict:
        dictOut['links'].append({
            'source': edge[0],
            'target': edge[1],
            'weight': edge_dict[edge]['weight']
        })
    
    return dictOut


def save_SingleGraph(filename, g):
    with open(filename,'w') as fileOut:
        fileOut.write(json.dumps(graph2dict(g)))
        fileOut.flush()
        fileOut.close()
    

def save_Graphs(path, name, gs, distance_scale):
    # save config
    with open("{0}{1}.json".format(path, name), 'w') as jsonOut:
        config = {
            "day_start": 1,
            "day_end": len(gs),
            "prefix": "{0}_".format(name),
            "distance_scale": distance_scale
        }
        jsonOut.write(json.dumps(config))
        jsonOut.flush()
        jsonOut.close()
    for day in range(0, len(gs)):
        save_SingleGraph("{0}{1}{2}.json".format(
            path, config['prefix'], day + 1), gs[day]
        )


