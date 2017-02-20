import pydot
import sys

g = pydot.graph_from_dot_data(open(sys.argv[1]).read())[0]

def make_vertex_pretty(v):
    label = '{}'.format(v.get_attributes()['label'].replace('"','').replace(',','').replace('I','keyitem'))
    if label == '':
        label = 'empty'
    return label + v.get_name()



def make_edge_pretty(e,vertices):
    label = ' -{}> '.format(e.get_attributes()['label'].replace('"','').replace(',','')).replace('I','item_locked')
    return  make_vertex_pretty(vertices[int(e.get_source())]) + label + make_vertex_pretty(vertices[int(e.get_destination())])


#for v in g.get_nodes():
#    print make_vertex_pretty(v)

nodes = {int(n.get_name()):n for n in g.get_nodes()}

print '{\n\t'+',\n\t'.join([ make_edge_pretty(e,nodes) for e in g.get_edges()]) + ';\n}\n'
   
