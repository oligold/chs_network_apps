'''
Created on Aug 20, 2015

@author: olivier

Module to test web algorithms
'''
import graph,web_algorithms
import graph_animation as granim
# import graph_utilities as gutil
import sys

choices = ['RANDOMST','EXTREMEST']
choiceIdx = 1
g = graph.Graph()
g.read_graph('graphs/planar_dir_5.txt')
''' Generate a directed graph '''
# g.generate_planar_graph(30,0.5,True)
# g.save_graph('graphs/planar_dir_30.txt')
walk_anim = web_algorithms.random_walk(g,10000)
# web_algorithms.in_degrees(g)
g.draw(None,None,True)
g.show()
# granim.animate(g,walk_anim,granim.animate_func_erase,None,'blue',100,True)