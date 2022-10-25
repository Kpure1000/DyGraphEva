import json

def proc(s, t, w, d):
    return {'s':s, 't':t,'w':w,'d':d}

def procc(el):
    print(el)
    return {'s':el}

with open("../data/dataset/truth/mammalia-pa/mammalia-pa.edges", 'r') as f:
    l = [[ el for el in line.split(' ') ] for line in f]

l.sort(key=lambda li: int(li[3]), reverse=False)

edge_day={}
node_set=set()
for ll in l:
    if int(ll[3]) not in edge_day:
        edge_day[int(ll[3])]=[]
    edge_day[int(ll[3])].append({
        'source': int(ll[0]),
        'target': int(ll[1]),
        'weight': float(ll[2])
    })
    node_set.add(int(ll[0]))
    node_set.add(int(ll[1]))

nodes = [{'id': n, 'group': 0} for n in node_set]
days=list(edge_day)
for d in range(0, len(days)):
    with open("../data/dataset/truth/mammalia-pa/mammalia-pa_{0}.json".format(d+1),'w') as f:
        day_graph = {'nodes': nodes, 'links': edge_day[days[d]]}
        f.write( json.dumps(day_graph) )
        f.flush()
        f.close()


