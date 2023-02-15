import networkx as nx
import pandas


def save_graph(g, days):
    import json
    g_json = {
        'nodes': [],
        'links': [],
    }

    nodes = dict(g.nodes)

    for node in nodes:
        g_json["nodes"].append({
            "id": node,
            "group": 0,
        })

    for edge in g.edges(data=True):
        g_json["links"].append({
            "source": edge[0],
            "target": edge[1],
            "weight": edge[2]["weight"],
        })

    with open("../../data/dataset/truth/ambassador/ambassador_{0}.json".format(days),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()


def csv2graph(d):
    nd = d.to_numpy()
    # src tar w
    G = nx.Graph()
    for r in nd:
        G.add_edge(int(r[0]), int(r[1]), weight = float(r[2]))
    return G



names = ['1985_1989','1990_1994','1995_1999','2000','2001','2002']

Gs = [csv2graph(pandas.read_csv(f'../../data/dataset/truth/ambassador/{n}.csv')) for n in names]

# [12,3,11,1,2,0,5,14,4]

for g in Gs:
    g.remove_nodes_from(set(g.nodes) - set([12,3,11,1,2,0,5,14,4]))

for i, g in enumerate(Gs):
    save_graph(g, i)
