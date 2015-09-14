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
            shpath, _animres = transport_algorithms.dijkstra(g, src, snk)
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

    def run_simulation(self):
        simTime = 0
        animate = []
        while True:
#             if simTime % 10 == 0:
#                 print 'Simulation time is %d' % simTime
            if len(self.cars) == 0:
                break
            simTime += 1
            for car in self.cars:
                if car.startTime > simTime:
                    ''' Car hasn't started yet '''
                    continue
                if car.startTime == simTime:
                    ''' Check if the start position is occupied '''
                    if car.route[0].occ[0]:
                        car.startTime += 1
                        continue
                    car.pos = (0,0)
                    print '\tCar %d has started at time %d' % (car.idx,simTime)
                    car.route[0].occ[0] = car
                    continue
                if car.startTime < simTime:
                    ''' Check if the car is stopped and start it if next
                        position is free but don't move it yet '''
                    if car.stopped:
                        (rd,seg) = car.get_next_pos()
                        if rd == -1:
                            ''' Car has almost reached its destination'''
                            car.stopped = False
                            continue
                        elif car.route[rd].occ[seg]:
                            ''' There is a car in the next segment '''
                            continue
                        else:
                            car.stopped = False
#                             print 'Car %d has restarted at time %d' % (car.idx,simTime)
                            continue
                    else:
                        ''' Car is not stopped '''
                        (rd,seg) = car.get_next_pos()
                        if rd == -1:
                            ''' Car has arrived at destination '''
                            car.free_current_position()
                            print '\tCar %d has arrived at time %d' % (car.idx,simTime)
                            self.cars.remove(car)
                            continue
                        elif car.route[rd].occ[seg]:
                            ''' There is a car in the next segment '''
                            car.stopped = True
                            print 'Car %d has stopped at time %d' % (car.idx,simTime)
                            continue
                        else:
                            ''' Move the car of one unit '''
                            car.move_car()
                            (currd,curseg) =  car.pos
                            car.route[currd].occ[curseg] = None
                            car.pos = (rd,seg)
                            car.route[rd].occ[seg]
            if not simTime % 3 == 0:
                continue
            car_pos = []
            for car in self.cars:
                (x,y) = car.get_coors()
                if x > -1:
                    car_pos.append((x,y))
            animate.append(car_pos)
        return animate
                    

        