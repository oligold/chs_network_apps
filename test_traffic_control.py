'''
Created on Sep 13, 2015

@author: olivier
'''
import graph,transport_algorithms
import graph_animation as granim
import simulate_traffic
# import graph_utilities as gutil
# import graph_utilities as gutil
import sys
row_nb = 10
car_count = 1
g = graph.Graph()
g.generate_grid_graph(row_nb,0.45)
g.save_graph('graphs/gridgraph_%d.txt' % row_nb**2)
msg = 'Grid graph on %d nodes' % row_nb**2
g.draw(msg)
g.print_graph('results/gridgraph_%d.png' % row_nb**2)
sim = simulate_traffic.SimulateTraffic(g,car_count)
animate = sim.run_simulation()
# granim.animate_car(g,animate,granim.animate_func_car,None,'blue',100,True)
granim.create_car_movie(g,'car_animation_%d' % car_count,animate,granim.animate_func_car)

# for ix in range(10):
#     g.read_graph('graphs/gridgraph_%d.txt' % row_nb**2)
#     flag = True
#     while flag:
#         flag = False
#         src = g.get_random_node()
#         snk = g.get_random_node()
#         if src == snk:
#             flag = True
#     shpath, _animres = transport_algorithms.dijkstra(g, snk, src)
#     if shpath == None:
#         print 'No shortest path between %d and %d' % (src.idx,snk.idx)
#         continue
#     src.color = 'green'
#     snk.color = 'blue'
#     for (e,e_ln) in shpath:
#         e.color = 'red'
#         e.width = 2
#     msg = 'path from (%d,%d) to (%d,%d)' % (src.idx/row_nb,src.idx%row_nb,snk.idx/row_nb,snk.idx%row_nb)
#     g.draw(msg)
#     g.print_graph('results/gridgraph_%d_%d.png' % (row_nb**2,ix+1))
    
