'''
Created on Sep 13, 2015

@author: olivier
'''
import graph,transport_algorithms
import graph_animation as granim
import simulate_traffic
import carclass
# import graph_utilities as gutil
# import graph_utilities as gutil
import sys
row_nb = 20
car_count = 500
g = graph.Graph()
g.generate_grid_graph(row_nb,0.45)
g.save_graph('graphs/gridgraph_%d.txt' % row_nb**2)
# msg = 'Grid graph on %d nodes' % row_nb**2
# g.draw(msg)
# g.print_graph('results/gridgraph_%d.png' % row_nb**2)
sim = simulate_traffic.SimulateTraffic(g,car_count)
carclass.VARIABLE_SIGNAL = False
animate = sim.run_simulation()
carclass.VARIABLE_SIGNAL = True
animate = sim.run_simulation()
granim.animate_car(g,animate,granim.animate_func_car,None,'blue',500,True)
# granim.create_car_movie(g,'car_animation_%d' % car_count,animate,granim.animate_func_car)
