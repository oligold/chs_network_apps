'''
Created on Aug 16, 2015

@author: olivier
'''
import node,edge
import random,math
import sys
import matplotlib.pyplot as plt
# import matplotlib.animation as animation

class Graph:
    '''
    implement graphs function
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.edges = []
        self.nodes = {}
        ''' dictionary of edges '''
        self.edgedic = None
        self.directed = False
    
    ''' return the dictionary of nodes '''
    def get_nodes(self):
        return self.nodes
    
    ''' return the list of edges '''
    def get_edges(self):
        return self.edges
    ''' return the edge between node nd1 and nd2 or None if not found '''
    def find_edge(self,nd1,nd2):
        ''' Build edge dictionary if not found '''
        if not self.edgedic:
            self.edgedic = {}
            for e in self.edges:
                self.edgedic[(e.orig,e.dest)] = e
                self.edgedic[(e.dest,e.orig)] = e
        if (nd1,nd2) in self.edgedic:
            return self.edgedic[(nd1,nd2)]
        else:
            return None
    '''
    Return a random node in the graph
    '''
    def get_random_node(self):
        ix = int(len(self.nodes.keys())*random.random())
        return self.nodes[ix]
    
    ''' return the node that is closest to the lower left corner '''
    def get_source(self):
        mini = sys.maxint
        theNode = None
        for key in self.nodes.keys():
            if self.nodes[key].x+self.nodes[key].y <mini:
                mini = self.nodes[key].x+self.nodes[key].y
                theNode = self.nodes[key]
        return theNode
    
    ''' return the node that is closest to the upper right corner '''
    def get_sink(self):
        maxi = 0
        theNode = None
        for key in self.nodes.keys():
            if self.nodes[key].x+self.nodes[key].y > maxi:
                maxi = self.nodes[key].x+self.nodes[key].y
                theNode = self.nodes[key]
        return theNode
    
    ''' Generate a set of nodes randomly distributed in the unit square '''
    def generate_nodes(self,node_count):
        self.nodes = {}
        for ix in range(node_count):
            self.nodes[ix] = node.Node(0.01+0.97*random.random(),0.01+0.97*random.random())
    
    ''' Generate a complete graph on node_count vertices '''
    def generate_complete_graph(self,node_count):
        self.generate_nodes(node_count)
        self.edges = []
        for ix1 in range(node_count):
            for ix2 in range(ix1+1,node_count):
                e = edge.Edge(self.nodes[ix1],self.nodes[ix2])
                e.length = self.distance(self.nodes[ix1],self.nodes[ix2])
                e.color = 'white'
                self.edges.append(e)
    
    ''' Return complete list of pair of nodes with distances '''
    def get_node_dist_dic(self):
        pair_dic = {}
        for ix1 in range(len(self.nodes)):
            for ix2 in range(ix1+1,len(self.nodes)):
                dist = self.distance(self.nodes[ix1], self.nodes[ix2])
                pair_dic[dist] = (ix1,ix2)
        return pair_dic
            
    
    
    ''' Generate a planar graph on node_count vertices '''
    def generate_planar_graph(self,node_count,prob,directed = False):
        if directed:
            self.directed = True
        self.generate_nodes(node_count)
        self.edges = []
        pair_dic = self.get_node_dist_dic()
        keys = pair_dic.keys()
        keys.sort()
        for key in keys:
            (ix1,ix2) = pair_dic[key]
            e = edge.Edge(self.nodes[ix1],self.nodes[ix2])
            if not self.does_edge_intesect(e):
                if random.random()< prob:
                    e.length = self.distance(self.nodes[ix1],self.nodes[ix2])
                    self.edges.append(e)
                if directed and random.random() < prob:
                    e = edge.Edge(self.nodes[ix2],self.nodes[ix1])
                    e.length = self.distance(self.nodes[ix2],self.nodes[ix1])
                    self.edges.append(e)
    
    ''' Compute adjacencies:
        find neighbors of each vertex '''
    def compute_adjacencies(self,from_node = False):
        for key in self.nodes.keys():
            self.nodes[key].neighs = []
        for e in self.edges:
            orig,dest = e.orig,e.dest
            if not self.directed or (self.directed and from_node):
                orig.neighs.append(e)
            if not self.directed or (self.directed and not from_node):
                dest.neighs.append(e)
        return
    
    ''' Remove isolated vertices '''
    def remove_isolated_vertices(self):
        self.compute_adjacencies()
        isolated_count = 0
        for key in self.nodes.keys():
            if len(self.nodes[key].neighs) == 0:
                isolated_count += 1
                del self.nodes[key]
        print '%d isolated nodes were removed' % isolated_count
        return
            
    
    ''' Generate a geometric graph on node_count vertices:
        two nodes are connected by an edge if their distance is less than max_dist
    '''
    def generate_geometric_graph(self,node_count,max_dist,directed = False):
        if directed:
            self.directed = True
        self.generate_nodes(node_count)
        self.edges = []
        for ix1 in range(node_count):
            for ix2 in range(ix1+1,node_count):
                if self.distance(self.nodes[ix1],self.nodes[ix2]) < max_dist:
                    e = edge.Edge(self.nodes[ix1],self.nodes[ix2])
                    e.length = self.distance(self.nodes[ix1],self.nodes[ix2])
                    self.edges.append(e)
    
    ''' Compute the distance between two nodes '''
    def distance(self,nd1,nd2):
        x1,y1 = nd1.x,nd1.y
        x2,y2 = nd2.x,nd2.y
        return math.sqrt((x1-x2)**2+(y1-y2)**2)
    
    ''' Verify that a potential edge intersect with another edge '''
    def does_edge_intesect (self,etest):
        for e in self.edges:
            if self.intersect(etest,e):
                return True
        return False

    ''' Verify if two edges intersect '''
    def intersect(self,e1,e2):
        nd1,nd2 = e1.orig,e1.dest
        nd3,nd4 = e2.orig,e2.dest
        ''' Verify that edges are not incident '''
        if nd1 == nd3 or nd1 == nd4 or nd2 == nd3 or nd2 == nd4:
            return False
        pt1h,pt1v = nd1.x,nd1.y
        pt2h,pt2v = nd2.x,nd2.y
        pt3h,pt3v = nd3.x,nd3.y
        pt4h,pt4v = nd4.x,nd4.y
        a1= (pt1v-pt2v)/(pt1h-pt2h)
        b1= pt1v - a1*pt1h
        a2= (pt3v-pt4v)/(pt3h-pt4h)
        b2= pt3v-a2*pt3h
        pt5h = (b2-b1)/(a1-a2)
        pt5v = a1*pt5h+b1
        if (pt5h < pt1h and pt5h < pt2h) or (pt5h > pt1h and pt5h > pt2h):
            return False
        if (pt5v < pt1v and pt5v < pt2v) or (pt5v > pt1v and pt5v > pt2v):
            return False
        if (pt5h < pt3h and pt5h < pt4h) or (pt5h > pt3h and pt5h > pt4h):
            return False
        if (pt5v < pt3v and pt5v < pt4v) or (pt5v > pt3v and pt5v > pt4v):
            return False
        return True
    
    ''' Save graph '''
    def save_graph(self,filename):
        if not filename.endswith('.txt'):
            filename.split('.')[0]+'.txt'
        f = open(filename,'w')
        if self.directed:
            f.write('DIRECTED\n')
        f.write('NODES\n')
        for key in self.nodes.keys():
            nd = self.nodes[key]
            nd.idx = key
            f.write("%d,%.4f,%.4f\n" % (nd.idx,nd.x,nd.y))
        f.write('EDGES\n')
        for e in self.edges:
            f.write("%d,%d,%.4f\n" % (e.orig.idx,e.dest.idx,e.length))
        f.close()
        return

    ''' Read graph '''
    def read_graph(self,filename):
        self.nodes = {}
        self.edges = []
        f = open(filename,'r')
        lines = f.readlines()
        f.close()
        flag = 0
        ndIdx = 0
        for line in lines:
            line = line.rstrip('\n\r')
            if line.startswith('DIRECTED'):
                self.directed = True
                continue
            if line.startswith('NODES'):
                flag = 1
                continue
            if line.startswith('EDGES'):
                flag = 2
                continue
            if flag == 0:
                continue
            segs = line.split(',')
            if len(segs) < 3:
                continue
            if flag == 1:
                self.nodes[int(segs[0])] = node.Node(float(segs[1]),float(segs[2]))
                self.nodes[int(segs[0])].idx = ndIdx
                ndIdx += 1
                continue
            if flag == 2:
                e = edge.Edge(self.nodes[int(segs[0])],self.nodes[int(segs[1])])
                e.length = float(segs[2])
                if filename.find('complete') > -1:
                    e.color = 'white'
                self.edges.append(e)
                
        return
    
    '''
    Plot one node
    '''
    def plot_node(self,node,globalColor = None,txt = False):
        x,y = node.x,node.y
        if not globalColor:
            col = node.color
        else:
            col = globalColor
        if txt:
            plt.text(x,y,str(node.idx),color='black', fontsize=10)
        else:
            plt.plot(x, y, 'ro',color=col)
        return

    '''
    Plot all nodes
    '''
    def plot_nodes(self,globalColor = None,txt = False):
        for key in self.nodes.keys():
            if self.nodes[key].idx == -1:
                self.nodes[key].idx = key
            self.plot_node(self.nodes[key],globalColor,txt)
        return
    
    '''
    Plot one edge
    '''
    def plot_edge(self,e,globalColor=None,globalWidth=None):
        orig,dest = e.orig,e.dest
        if not globalColor:
            col = e.color
        else:
            col = globalColor
        if not globalWidth:
            width = e.width
        else:
            width = globalWidth
        if self.directed:
            plt.arrow(orig.x,orig.y,dest.x-orig.x,dest.y-orig.y,color=col, 
                      head_width=0.01, head_length=0.02,
                      length_includes_head = True,linewidth=width)
        else:
            plt.plot([orig.x,dest.x],[orig.y,dest.y],color=col, linewidth=width)
        return

    '''
    Plot all edges
    '''
    def plot_edges(self,globalColor = None):
        for e in self.edges:
            if e.color == 'white':
                continue
            self.plot_edge(e,globalColor)
        return
    '''
    Draw graph
    '''
    def draw(self,msg = None, globalColor = None,txt = False):
        self.plot_edges(globalColor)
        self.plot_nodes(globalColor,txt)
        if msg:
            plt.text(0,0,msg,color='black', fontsize=12)
    '''
    Show graph
    '''
    def show(self):
        plt.show()
    

        