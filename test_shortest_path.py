'''
Created on Aug 20, 2015

@author: olivier
Function to test the shorest path algorithm
'''
import graph,transport_algorithms
import graph_animation as granim
# import graph_utilities as gutil
import sys

choices = ['RANDOMST','EXTREMEST']
choiceIdx = 1
g = graph.Graph()
g.read_graph('graphs/planar_30.txt')
# g.generate_planar_graph(30,0.7)
# g.save_graph('graphs/planar_30.txt')
g.remove_isolated_vertices()
if choiceIdx == 0:
    src = snk = None
    while src == snk:
        src = g.get_random_node()
        snk = g.get_random_node()
elif choiceIdx == 1:
    src = g.get_source()
    snk = g.get_sink()
src.color = 'red'
snk.color = 'red'
shortest_path,animation_lst = transport_algorithms.dijkstra(g, src, snk,False)
if not shortest_path:
    sys.exit()
path_length = 0
for (e,ln) in shortest_path:
    path_length += ln
animation_lst.append(shortest_path)
msg = 'Path has length %.2f' % path_length
granim.animate(g,animation_lst,granim.animate_func,msg,'red')
