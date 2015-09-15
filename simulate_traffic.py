'''
Created on Sep 13, 2015

@author: olivier
'''
import carclass
import transport_algorithms

class SimulateTraffic(object):
    '''
    Run the traffic simulation
    '''
    


    def __init__(self, g, car_count):
        '''
        Constructor
        g is the graph on which traffic is simulated
        car_count is the number of cars
        '''
        self.cars = []
        startTime = 0
        ''' Initialize the cars '''
        while len(self.cars) < car_count:
            flag = True
            while flag:
                flag = False
                src = g.get_random_node()
                snk = g.get_random_node()
                if src == snk:
                    flag = True
            shpath, _animres = transport_algorithms.dijkstra(g, src, snk, fromNode = False)
            if shpath == None:
                continue
            route = []
            '''compute the route of the car '''
            for (e,_eln) in shpath:
                route.append(e)
            ''' Add one second to the start time '''
            startTime += 1
            car = carclass.Car(route,startTime)
            car.idx = startTime
            self.cars.append(car)
        ''' Reset node weights to zero'''
        for ix in g.get_nodes():
            g.nodes[ix].weight = -1

    def run_simulation(self):
        simTime = 0
        animate = []
        arrivedcars_count = 0
        for car in self.cars:
            car.reset()
        while True:
#             if simTime % 10 == 0:
#                 print 'Simulation time is %d' % simTime
            if len(self.cars) == arrivedcars_count:
                break
            simTime += 1
            for car in self.cars:
                if car.arrivalTime > -1:
                    continue
                if car.startTime > simTime:
                    ''' Car hasn't started yet '''
                    continue
                if car.startTime == simTime:
                    ''' Check if the start position is occupied '''
                    if car.route[0].occ[0]:
                        car.startTime += 1
                        continue
                    car.pos = (0,0)
#                     print '\tCar %d has started at time %d' % (car.idx,simTime)
                    car.route[0].occ[0] = car
                    continue
                if car.startTime < simTime:
                    ''' Check if the car is stopped and start it if next
                        position is free but don't move it yet '''
                    if car.stopped:
                        (rd,seg,siggreen) = car.get_next_pos(simTime)
                        if rd == -1:
                            ''' Car has almost reached its destination'''
                            car.stopped = False
                            continue
                        elif car.route[rd].occ[seg] or not siggreen:
                            ''' There is a car in the next segment '''
                            continue
                        else:
                            car.stopped = False
#                             print 'Car %d has restarted at time %d' % (car.idx,simTime)
                            continue
                    else:
                        ''' Car is not stopped '''
                        (rd,seg,siggreen) = car.get_next_pos(simTime)
                        if rd == -1:
                            ''' Car has arrived at destination '''
                            car.free_current_position()
                            car.arrivalTime = simTime
#                             print '\tCar %d has arrived at time %d' % (car.idx,simTime)

                            arrivedcars_count += 1
#                             print 'Number of arrived cars is '+str(arrivedcars_count)
                            continue
                        elif car.route[rd].occ[seg] or not siggreen:
                            ''' There is a car in the next segment '''
                            car.stopped = True
#                             print 'Car %d has stopped at time %d' % (car.idx,simTime)
                            continue
                        else:
                            ''' Move the car of one unit '''
                            car.move_car()
                            (currd,curseg) =  car.pos
                            car.route[currd].occ[curseg] = None
                            car.pos = (rd,seg)
                            car.route[rd].occ[seg]
            if not simTime % 5 == 0:
                continue
            car_pos = [simTime]
            for car in self.cars:
                (x,y) = car.get_coors()
                if x > -1:
                    if car.stopped:
                        car_pos.append((x,y,'red'))
                    else:
                        car_pos.append((x,y,'blue'))
            animate.append(car_pos)
        ''' Now we compute for each car the extra time spent on the road '''
        perc_lst = []
        for car in self.cars:
            minTime = 50*len(car.route)+1
            actualTime = car.arrivalTime-car.startTime
            carPerc = 100*float(actualTime-minTime)/minTime
            perc_lst.append(carPerc)
#             print 'Car %d took %d actual time and was %.2f percent over minimum time' % \
#                 (car.idx,actualTime,carPerc)
        average = sum(perc_lst)/len(self.cars)
        variance = sum((average - value) ** 2 for value in perc_lst) / len(self.cars)
        print "Average percentage of travel time over minimum is %.2f" % average
        print "Variance percentage of travel time over minimum is %.2f" % variance
        return animate
                    

        