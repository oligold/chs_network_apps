'''
Created on Aug 31, 2015

@author: olivier
'''
import graph,social_network_growth
import graph_animation as granim
# import graph_utilities as gutil
# import sys

g = graph.Graph()
g.read_graph('graphs/complete_100.txt')
# g.generate_complete_graph(100)
# g.save_graph('graphs/complete_100.txt')
lst_anim = social_network_growth.grow_social_network(g)

# g.draw()
# g.print_graph('results/socialgrowth_100.png')
msg = 'red:strong, black:weak, blue:strong-triad, green:weak-triad, conn_count: %d' % len(lst_anim)
granim.create_movie(g,'socialgrowth_notriad_100',lst_anim,granim.animate_func_evolv,msg,'blue')
# granim.animate(g,walk_anim,granim.animate_func_erase,None,'blue',100,True)