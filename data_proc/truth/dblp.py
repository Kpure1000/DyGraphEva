from xml.dom.minidom import parse
from xml.dom.minidom import Document

import networkx as nx
import matplotlib.pyplot as plt

def readSingle(filename):
    tree = parse(f"../../data/dataset/truth/dblp/{filename}.xml")
    hits = tree.getElementsByTagName('hit')
    au_papers = {}
    G = nx.Graph()
    for hit in hits:
        authors = {author.getAttribute('pid'): author.firstChild.data
            for author in hit.getElementsByTagName('author')}
        title = hit.getElementsByTagName('title')[0].firstChild.data
        aul = list(authors)
        for au in aul:
            if au not in au_papers:
                au_papers[au] = 1
            else:
                au_papers[au] += 1

        for i in range(len(aul)):
            for j in range(i):
                if aul[i] not in G:
                    G.add_node(aul[i], author=authors[aul[i]])
                if aul[j] not in G:
                    G.add_node(aul[j], author=authors[aul[j]])
                if G.has_edge(aul[i], aul[j]):
                    G[aul[i]][aul[j]]['weight'] += 1
                    G[aul[i]][aul[j]]['title'] += f"#{title}"
                else:
                    G.add_edge(aul[i], aul[j], title=title, weight=1)

    nx.set_node_attributes(G, au_papers, 'papers')

    return G

def co_author_filter(G_org, filter_func):
    aus_filt = [
        node for node in G_org.nodes if filter_func(G_org, node) == True
    ]
    # print(f"tot aus: {len(G_org)}")
    # print(f"eff aus: {len(eff_aus)}")
    G = nx.Graph()
    for i in range(len(aus_filt)):
        for j in range(i):
            if aus_filt[i] not in G:
                G.add_node(aus_filt[i],
                author=G_org.nodes[aus_filt[i]]['author'],
                papers=G_org.nodes[aus_filt[i]]['papers'])
            if aus_filt[j] not in G:
                G.add_node(aus_filt[j],
                author=G_org.nodes[aus_filt[j]]['author'],
                papers=G_org.nodes[aus_filt[j]]['papers'])
            if G_org.has_edge(aus_filt[i], aus_filt[j]):
                G.add_edge(aus_filt[i], aus_filt[j],
                           title=G_org[aus_filt[i]][aus_filt[j]]['title'],
                           weight=float(G_org[aus_filt[i]][aus_filt[j]]['weight']))

    return G



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
            "author": nodes[node]['author'],
            "papers": nodes[node]['papers'],
        })

    for edge in g.edges(data=True):
        g_json["links"].append({
            "source": edge[0],
            "target": edge[1],
            "weight": edge[2]["weight"],
            "title": edge[2]["title"],
        })

    with open("../../data/dataset/truth/dblp/dblp_{0}.json".format(days),'w') as file:
        file.write( json.dumps(g_json) )
        file.close()



years = ['2019', '2020', '2021', '2022']


Gs = [readSingle(y) for y in years]

GFs = [co_author_filter(G, lambda _org, node: _org.nodes[node]['papers'] >= 1) for G in Gs]

co_set=set()
for i, G in enumerate(GFs):
    nodes_sets = nx.connected_components(G)
    max_comp = max(nodes_sets, key=lambda ele: len(ele))
    if i == 0:
        co_set = max_comp
    else:
        co_set = max_comp & co_set

co_list=[co for co in co_set]

subGFs = [nx.subgraph(GF, nbunch=co_set) for GF in GFs]

# for i,g in enumerate(GFs):
#     au_lables = nx.get_node_attributes(g, 'papers')
#     if i != 0:
#         plt.figure()
#     nx.draw_networkx(g, labels=au_lables)
# plt.show()

for i,g in enumerate(subGFs):
    save_graph(g, i + int(years[0]))
