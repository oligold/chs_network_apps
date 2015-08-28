'''
Created on Aug 16, 2015

@author: olivier
Test the graph functions
'''
import graph,transport_algorithms
import graph_animation as granim
# import graph_utilities as gutil
import sys

# choices = ['CONVEXHULL','CONVEXHULL2XCHANGE','NEXTCLOSEST','NEXTCLOSEST2XCHANGE']
choices = ['NEXTCLOSEST2XCHANGE']
g = graph.Graph()
g.generate_complete_graph(100)
g.save_graph('graphs/complete_100.txt')
# g = graph.Graph()
# g.read_graph('graphs/complete_200.txt')
for choice in choices:
    if choice == 'CONVEXHULL' or choice == 'CONVEXHULL2XCHANGE':
        tour,tsp_anim = transport_algorithms.tsp_convex_hull(g)
        if choice == 'CONVEXHULL2XCHANGE':
            tour,new_tsp_anim = transport_algorithms.tsp_2_exchange(g, tour)
            tsp_anim.extend(new_tsp_anim)
    elif choice == 'NEXTCLOSEST' or choice == 'NEXTCLOSEST2XCHANGE':
        tour,tsp_anim = transport_algorithms.tsp_closest(g)
        if choice == 'NEXTCLOSEST2XCHANGE':
            tour,new_tsp_anim = transport_algorithms.tsp_2_exchange(g, tour)
            tsp_anim.extend(new_tsp_anim)
            
    if not tour:
        print 'Could not find a convex hull for the graph'
        sys.exit()
    tsp_length = 0
    for ix in range(len(tour)):
        e = g.find_edge(tour[ix],tour[(ix+1) % len(tour)])
        if not e:
            continue
        tsp_length += e.length
    msg = choice+' TSP tour length is %.2f' % tsp_length
    # granim.create_movie(g,tsp_anim,granim.animate_func_erase,msg,'blue')
    for ix in range(len(tour)):
        e = g.find_edge(tour[ix],tour[(ix+1) % len(tour)])
        if not e:
            continue
        e.color = 'blue'
    g.draw(msg)
    g.print_graph('results/complete_100.png')
