from asyncio.windows_events import NULL
import json
import xmltodict

# uni_obj = xmltodict.parse("../data/dataset/truth/newcomb/NewcombFraternity.xml")

in_obj={}

with open("../data/dataset/truth/newcomb/NewcombFraternity.xml", 'r') as filein:
    in_obj = xmltodict.parse(filein.read(), attr_prefix='')
    filein.close()

# deal nodes
nodes = in_obj['DynamicNetwork']['MetaNetwork']['nodes']['nodeclass']['node']

for node in nodes:
    node['id'] = int(node['id'])  # integral id
    node['group'] = 0            # a group

# deal days and links
days = in_obj['DynamicNetwork']['MetaNetwork']['networks']['network']
days_net = []
for day in days:
    for network in day['link']:
        network['source'] = int(network['source'])
        network['target'] = int(network['target'])
        network['weight'] = int(network['value'])
        network.pop('value')
        network.pop('type')

    links = {}
    links['links'] = day['link']
    days_net.append(links)

day_index = 1
for day_net in days_net:
    out_obj = {}
    out_obj['nodes'] = nodes
    out_obj['links'] = day_net['links']
    
    json_str = json.dumps(out_obj)
    
    with open("../data/dataset/truth/newcomb/newcomb_{0}.json".format(day_index), 'w') as fileout:
        fileout.write(json_str)
        fileout.flush()
        fileout.close()

    day_index+=1