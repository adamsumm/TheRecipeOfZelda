class Vertex:
    def __init__(self,id=0,label=''):
        self.label = label
        self.id = id
    def __str__(self):
        return str(self.label) + str(self.id)
    
class Edge:
    def __init__(self,v1,v2,label=''):
        self.v1 = v1
        self.v2 = v2
        self.label = label
    def __str__(self):
        return str(self.v1) + '-'+str(self.label)+'->'+str(self.v2)
class Graph:
    
    
    def __init__(self,vertices,edges):
        self.vertices = [v for v in vertices]
        self.edges = [e for e in edges]
        for e in edges:
            if e.v1 not in self.vertices:
                self.vertices.append(e.v1)
            if e.v2 not in self.vertices:
                self.vertices.append(e.v2)
            
        self.v2e = {v:{v2:set() for v2 in vertices} for v in vertices}
        for e in edges:
            self.v2e[e.v1][e.v2].add(e)

    def renumber(self):
        for i,v in enumerate(self.vertices):
            v.id = i
            
    def add_vertex(self,v):
        self.vertices.append(v)
        self.v2e[v] = {v2:set() for v2 in self.vertices}
        for o in self.vertices:
            self.v2e[v][o] = set()
            self.v2e[o][v] = set()
    
    def add_edge(self,v1,v2,label):
        self.edges.append(Edge(v1,v2,label))
        self.v2e[v1][v2].add(self.edges[-1])
    def clone(self):
        mapping = {}
        vertices = []
        for v in self.vertices:
            vertices.append(Vertex(v.id,v.label))
            mapping[v] =vertices[-1]
        edges = []
        for e in self.edges:
            edges.append(Edge(mapping[e.v1],mapping[e.v2],e.label))
        return Graph(vertices,edges)
        
    def find_vertex(self,id):
        for v in self.vertices:
            if v.id == id:
                return v
        return None
    def remove_vertex(self,v,prune=True):
        self.vertices.remove(v)

        into = []
        out_from = []
        if not prune:
            for o in self.v2e[v]:
                for e in self.v2e[v][o]:
                    out_from.append(e)
            for o in self.v2e:
                for e in self.v2e[o][v]:
                    into.append(e)
        
            
        del self.v2e[v]
        for o in self.v2e:
            del self.v2e[o][v]

        if not prune:
            for e_i in into:
                for e_o in out_from:
                    already_exists = False
                    for e in self.v2e[e_i.v1][e_o.v2]:
                        if e.label == e_o.label:
                            already_exists = True
                            break
                    if not already_exists and e_i.v1 != e_o.v2:
                        self.add_edge(e_i.v1,e_o.v2,e_o.label)
        to_remove = []
        for e in self.edges:
            if v == e.v1 or v == e.v2:
                to_remove.append(e)
        for e in to_remove:
            if e in self.edges:
                self.edges.remove(e)

        to_remove = set([])
        for ii in range(len(self.edges)):
            e1 = self.edges[ii]
            for jj in range(ii+1,len(self.edges)):
                e2 = self.edges[jj]
                if e1.label == e2.label and e1.v1 == e2.v1 and e1.v2 == e2.v2:
                    to_remove.add(e2)
                    
        for e in to_remove:
            if e in self.edges and e in self.v2e[e.v1][e.v2]:
                self.v2e[e.v1][e.v2].remove(e)
                self.edges.remove(e)
    def __str__(self):
        st = ''
        for v in self.vertices:
            st += 'vertex: '+str(v) + '\n'
        for e in self.edges:
            st += 'edge: ' +str(e) + '\n'
        return st
    def find_matches(self,other,vertex_equals=None,edge_equals=None):
        import itertools
        if len(self.vertices) < len(other.vertices):
            #print 'len bad'
            return []
        matches = []
        
        if not vertex_equals:
            vertex_equals = lambda x,y: x.label == y.label
        if not edge_equals:
            edge_equals = lambda x,y: (x.label == y.label and vertex_equals(x.v1,y.v1) and vertex_equals(x.v2,y.v2))
        possibles = [[v for v in self.vertices if vo.label == v.label] for vo in other.vertices]

        for perm in itertools.product(*possibles):
            if len(set(perm)) != len(perm):
                continue
        #for perm in itertools.permutations(self.vertices,len(other.vertices)):
            #is_good = True
            
            #for ind,v in enumerate(perm):
                #print ind,v
            #    if not vertex_equals(other.vertices[ind],v):
                    #print 'Nope'
            #        is_good = False
            #        break
            #if not is_good:
            #    continue
            is_good = len(other.edges) == 0
            mapping = {other.vertices[i]:v for i,v in enumerate(perm)}
            taken = set([])
            for edge in other.edges:
                o1 = mapping[edge.v1]
                o2 = mapping[edge.v2]
                is_good = False
                for e in self.v2e[o1][o2]:
                    
                    if e not in taken and edge_equals(edge,e):
                        #print 'G:',edge
                        #print 'SG:',e
                        taken.add(e)
                        is_good = True
                        break
                if not is_good:
                    break
                    
            if is_good:
                matches.append(perm)
                    
        return matches
    def to_dot(self):
        outstr = ['digraph {']
        mapping = {}
        for i,v in enumerate(self.vertices):
            mapping[v] = i
            outstr.append('{} [label="{}"]'.format(i,v.label))
        for e in self.edges:
            outstr.append('{} -> {} [label="{}"]'.format(mapping[e.v1],mapping[e.v2],e.label))
        outstr.append('}')
        return '\n'.join(outstr)
            
class Rule:
    def __init__(self,lhs,rhs,lhs_to_rhs,prune=True):
        self.lhs = lhs
        self.rhs = rhs
        self.prune = prune
        self.to_delete = [v for v in lhs.vertices if v not in lhs_to_rhs]
        self.lhs_to_rhs = lhs_to_rhs
        self.rhs_to_lhs = {r:l for l,r in lhs_to_rhs.items()}

        self.to_add = [v for v in rhs.vertices if v not in self.rhs_to_lhs]
        
        self.edges_to_delete = [e for e in lhs.edges if e not in lhs_to_rhs]
        
        self.edges_to_add = [e for e in rhs.edges if e not in self.rhs_to_lhs]
        
    def __str__(self):
        return 'RULE:\n' + str(self.lhs) + '\n=>\n'+ str(self.rhs) + '\n'
    def find_matches(self,other,vertex_equals=None,edge_equals=None):
        return other.find_matches(self.lhs,vertex_equals,edge_equals)
    def reverse(self):
        return Rule(self.rhs,self.lhs,self.rhs_to_lhs,prune=False)
    def apply_to(self,graph,match,vertex_equals=None,edge_equals=None):
        #print(self)
        mapping = {self.lhs.vertices[i]:v for i,v in enumerate(match)}
        #for l,r in self.lhs_to_rhs.items():
        #    print 'lhs', l, ' => ', r
        rhs_to_new = {}
        for v in self.to_add:
            new_v = Vertex(label=v.label)
            #print 'adding',new_v
            rhs_to_new[v] = new_v 
            graph.add_vertex(new_v)
        
        for e in self.edges_to_add:
            v1 = e.v1
            if v1 in self.rhs_to_lhs:
                v1 = mapping[self.rhs_to_lhs[v1]]
            else:
                v1 = rhs_to_new[v1]
            v2 = e.v2
            if v2 in self.rhs_to_lhs:
                v2 = mapping[self.rhs_to_lhs[v2]]
            else:
                v2 = rhs_to_new[v2]
            #new_e = Edge()
            #print 'adding ',v1, "-{}->".format(e.label),v2
            graph.add_edge(v1,v2,e.label)
                
            
        
        for e in self.edges_to_delete:
            #print 'deleting',e
            v1 = mapping[e.v1]
            v2 = mapping[e.v2]
            
            for oe in graph.v2e[v1][v2]:
                if oe.label == e.label:
                    graph.edges.remove(oe)
                    graph.v2e[v1][v2].remove(oe)
                    break
                
        for v in self.to_delete:
            #print 'deleting',v
            graph.remove_vertex(mapping[v],self.prune)
            
        for v in self.lhs_to_rhs:
            #print 'lhs->rhs',v,self.lhs_to_rhs[v]
            
            if v in self.lhs.vertices:
                if  'WILDCARD' not in self.lhs_to_rhs[v].label:
                    graph.vertices[graph.vertices.index(mapping[v])].label = self.lhs_to_rhs[v].label
            if v in self.lhs.edges:
                for oe in graph.v2e[mapping[v.v1]][mapping[v.v2]]:
                    if oe.label == v.label:
                        break
                    
                if  'WILDCARD' not in self.lhs_to_rhs[v].label:
                    oe.label =  self.lhs_to_rhs[v].label 
        
