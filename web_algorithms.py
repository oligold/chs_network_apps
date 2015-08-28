'''
Created on Aug 20, 2015

@author: olivier

Web network algorithms
'''

import random

'''
Random walk computes a weight on each node: number of times the
node was visited during the random walk.  From each node with visit 
a neighbor where all neighbors have equal probability to be visited.
If a node has no neighbor, then we restart the random node from 
a random node
'''
def random_walk(g,steps):
    ''' steps is the number of steps of the random walk '''
    if not g.directed:
        print 'Random walk works on a directed graph only'
        return
    for key in g.nodes.keys():
        g.nodes[key].weight = 0
    ''' Compute node adjancencies in the direction from -> to '''
    g.compute_adjacencies(True)
    nd = g.get_random_node()
    walk_anim = []
    e = None
    for _ix in range(steps):
        if len(nd.neighs) == 0:
            nd = g.get_random_node()
            continue
        if e:
            erase = [e]
        else:
            erase = []
        e = nd.neighs[int(random.random()*len(nd.neighs))]
        walk_anim.append((erase,[e]))
        
        nd = e.get_other_vertex(nd)
        nd.weight += 1
        continue
    ''' order the nodes by decreasing weights '''
    ordernd_lst = []
    for key in g.nodes.keys():
        ordernd_lst.append((g.nodes[key].weight,key))
    ordernd_lst.sort(reverse = True)
    idx = 0
    for (wt,key) in ordernd_lst:
        # print '%d %d' % (key,wt)
        idx += 1
        g.nodes[key].idx = idx
    return walk_anim
        
'''
InDegrees: we sort the nodes by decreasing values of in-degrees
'''
def in_degrees(g):
    if not g.directed:
        print 'InDegrees works on a directed graph only'
        return
    for key in g.nodes.keys():
        g.nodes[key].weight = 0
    ''' Compute the in-degree of each node '''
    for e in g.edges:
        e.dest.weight += 1
    ''' order the nodes by decreasing weights '''
    ordernd_lst = []
    for key in g.nodes.keys():
        ordernd_lst.append((g.nodes[key].weight,key))
    ordernd_lst.sort(reverse = True)
    idx = 0
    for (wt,key) in ordernd_lst:
        print '%d %d' % (key,wt)
        idx += 1
        g.nodes[key].idx = idx
    return
        
        