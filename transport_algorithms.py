'''
Created on Aug 18, 2015

@author: olivier

Code for some algorithms with transport
'''
import node
import heapq
import sys
import graph_utilities

''' Dijkstra finds the shortest path in a graph between a source and a sink vertex 
    If euclidean then use Euclidean distances else use number of hops'''
def dijkstra(g,src,snk,euclidean=True):
    ''' Compute adjacencies in the graph '''
    g.compute_adjacencies()
    ''' set all node weights to be infinity '''
    for key in g.nodes.keys():
        g.nodes[key].weight = sys.maxint
        g.nodes[key].seen = False
        g.nodes[key].next = None
    snk.weight = 0
    heap = []
    heapq.heappush(heap,(0,snk))
    animation_lst = []
    while 1 == 1:
        try:
            (price,node) = heapq.heappop(heap)
        except:
            break
        if not node == snk:
            animation_lst.append([(node.next,price)])
        if node.seen == True:
            continue
        node.seen = True
        if node == src:
            break
        # print node+" has "+str(len(node_dic[node].links))+" links"
        for e in node.neighs:
            other = e.get_other_vertex(node)
            if euclidean:
                weight = node.weight+e.length
            else:
                weight = node.weight+1
            if weight < other.weight:
                other.weight = weight
                other.next = e
                heapq.heappush(heap,(weight,other))
        continue
    ''' Check that source was reached (source is connected to sink by at least one path'''
    if not src.seen:
#         print 'Could not find a path between source and sink'
        return None,None
    node = src
    shortest_path = []
    while not node == snk:
        e = node.next
        shortest_path.append((e,e.length))
        node = e.get_other_vertex(node)
    return shortest_path,animation_lst

''' TSP from Convex Hull:
    This TSP heuristic works relatively well on graphs with Euclidean distances.
    1. Find a convex hull of the nodes
    2. Until all the nodes are in the TSP tour:
        2.1. Find the node N and TSP link (A,B) that minimizes the difference 
            (AN) + (NB) - (AB)
        2.2 Replace (A,B) with (A,N) and (N,B)
'''
def tsp_convex_hull(g):
    ''' Find the convex hull on the nodes on g '''
    convex_hull = graph_utilities.convexHull(g)
    if not convex_hull:
        return convex_hull
    write_edges = []
    for ix in range(len(convex_hull)):
        e = g.find_edge(convex_hull[ix],convex_hull[(ix+1) % len(convex_hull)])
        if e:
            write_edges.append(e)
    tsp_anim = []
    tsp_anim.append(([],write_edges))
    while len(convex_hull) < len(g.nodes):
        minDist = sys.maxint
        minNode = None
        hullNodeIdx = -1
        for key in g.nodes.keys():
            if g.nodes[key] in convex_hull:
                continue
            for ix in range(len(convex_hull)):
                dist = g.distance(g.nodes[key],convex_hull[ix]) \
                    + g.distance(g.nodes[key],convex_hull[(ix+1) % len(convex_hull)]) \
                    - g.distance(convex_hull[ix],convex_hull[(ix+1) % len(convex_hull)])
                if dist < minDist:
                    minNode = g.nodes[key]
                    minDist = dist
                    hullNodeIdx = ix+1
        erase_edge = [g.find_edge(convex_hull[hullNodeIdx-1],
                                  convex_hull[hullNodeIdx % len(convex_hull)])]
        write_edges = [g.find_edge(minNode,convex_hull[hullNodeIdx-1]),
                       g.find_edge(minNode,convex_hull[hullNodeIdx % len(convex_hull)])]
        tsp_anim.append((erase_edge,write_edges))
        convex_hull.insert(hullNodeIdx,minNode)
    return convex_hull,tsp_anim       
    
''' TSP from Closest neighbor:
    This TSP heuristic works starts from a random node and
    at each step moves to the closest unvisited neighbor.
'''
def tsp_closest(g,ndIdx = None):
    ''' Select a random node in g '''
    nodes = g.get_nodes()
    for key in nodes.keys():
        nodes[key].seen = False
    if ndIdx == None:
        nd = g.get_random_node()
    else:
        nd = nodes[ndIdx]
    nd.seen = True
    visited = [nd]
    tsp_anim = []
    while True:
        nd1 = visited[len(visited)-1]
        minDist = sys.maxint
        nd2 = None
        for key in nodes.keys():
            nd = nodes[key]
            if nd.seen:
                continue
            if g.distance(nd1,nd) < minDist:
                minDist = g.distance(nd1,nd)
                nd2 = nd
        if not nd2:
            break
        visited.append(nd2)
        nd2.seen = True
        e = g.find_edge(nd1,nd2)
        tsp_anim.append(([],[e]))
    e = g.find_edge(visited[len(visited)-1],visited[0])
    tsp_anim.append(([],[e]))
    return visited,tsp_anim 

''' In this heuristic we start from a TSP tour and try to improve the tour with 
    a series of 2-exchanges.  Let (a,b) and (c,d) be two connections of the TSP tour.
    If (a,c)+(b,d) < (a,b)+(c,d), then reverse the sequence from b to c.
'''
def tsp_2_exchange(g,tour):
    flag = True
    tsp_anim = []
    while flag:
        flag = False
        for ix1 in range(len(tour)-2):
            d1 = g.distance(tour[ix1],tour[ix1+1])
            for ix2 in range(ix1+2,len(tour)):
                d2 = g.distance(tour[ix2],tour[(ix2+1) % len(tour)])
                d3 = g.distance(tour[ix1],tour[ix2])
                d4 = g.distance(tour[ix1+1],tour[(ix2+1) % len(tour)])
                if d1+d2 > d3+d4:
#                     tourtxt = str(ix1)+' '+str(ix2)+' start'
#                     for nd in tour:
#                         tourtxt += ' '+str(nd.idx)
#                     print tourtxt
                    e1 = g.find_edge(tour[ix1],tour[ix1+1])
                    e2 = g.find_edge(tour[ix2],tour[(ix2+1) % len(tour)])
                    e3 = g.find_edge(tour[ix1],tour[ix2])
                    e4 = g.find_edge(tour[(ix2+1)%len(tour)],tour[ix1+1])
                    tsp_anim.append(([e1,e2],[e3,e4]))
                    for ix in range(ix2-ix1):
                        v = tour.pop(ix2)
                        tour.insert(ix1+1+ix,v)
#                         tourtxt = ''
#                         for nd in tour:
#                             tourtxt += ' '+str(nd.idx)
#                         print tourtxt
                    flag = True
                    break
            if flag:
                break
    return tour,tsp_anim
