'''
Created on Sep 13, 2015

@author: olivier
'''
from matplotlib.font_manager import path

VARIABLE_SIGNAL = False

class Car:
    '''
    Car class represent a vehicule travelling from one point to another.
    It drives at one road segment per second.  However if stopped it takes two second
    to reach the next segment.
    '''


    def __init__(self, route, startTime):
        '''
        Constructor
        path is the route of the car from origin to destination as a sequence of edges
        startTime is the starting time of the car from origin
        '''
        self.route = route
        self.startTime = startTime
        self.arrivalTime = -1
        ''' Position of the car as road and position on road '''
        self.pos = (-1,-1)
        self.idx = -1
        self.stopped = True
        
    def reset(self):
        self.stopped = True
        self.arrivalTime = -1
        self.startTime = self.idx
        self.pos = (-1,-1)
        
    def check_signal(self,e,simTime):
        ''' Verify if the signal is green or red.  If arriving intersection has less than
            two incoming roads, then the signal is green.  Else, signal is green if 
            direction of road is vertical and simtime is in first minute of pair of minutes
            or direction of road is horizontal and simtime is in second minute of pair 
            of minutes
        '''
        if VARIABLE_SIGNAL:
            return self.check_var_signal(e, simTime)
        sigphase = 120
        if not simTime:
            return True
        dest = e.dest
        orig = e.orig
        if len(dest.neighs) < 3:
            return True
        if orig.x == dest.x and simTime % sigphase < sigphase/2:
            return True
        if orig.y == dest.y and simTime % sigphase < sigphase \
            and simTime % sigphase >= sigphase/2:
            return True
        return False
    
    def check_var_signal(self,e,simTime):
        ''' Verify if the signal is green or red.  If arriving intersection has less than
            two incoming roads, then the signal is green.  Else, signal is green if 
            direction of road is vertical and simtime is in first minute of pair of minutes
            or direction of road is horizontal and simtime is in second minute of pair 
            of minutes
        '''
        minphase = 60
        if not simTime:
            return True
        dest = e.dest
        orig = e.orig
        if len(dest.neighs) < 3:
            return True
        if dest.weight == -1:
            dest.weight = simTime
            if orig.x == dest.x:
                dest.seen = True
            else:
                dest.seen = False
        if orig.x == dest.x:
            '''Vertical road '''
            if dest.seen:   
                return True
            else:
                ''' Can we turn the signal green?'''
                if simTime-dest.weight > minphase:
                    ''' Yes we can turn the signal '''
                    dest.seen = True
                    dest.weight = simTime
                    return True
                else:
                    return False
        else:
            ''' Horizontal road '''
            if not dest.seen:   
                return True
            else:
                ''' Can we turn the signal green?'''
                if simTime-dest.weight > minphase:
                    ''' Yes we can turn the signal '''
                    dest.seen = False
                    dest.weight = simTime
                    return True
                else:
                    return False
    
    def get_next_pos(self,simTime=None):
        ''' return car next position and indication if signal is red or green'''
        (i,j) = self.pos
        if j < self.route[i].length-1:
            return (i,j+1,True)
        elif i < len(self.route)-1:
            return (i+1,0,self.check_signal(self.route[i],simTime))
        else:
            ''' Car has arrived at destination '''
            return (-1,-1,True)
    ''' Move the car '''    
    def move_car(self):
        self.free_current_position()
        (i,j,_green) = self.get_next_pos()
        self.route[i].occ[j] = self
        
    ''' Free current position '''   
    def free_current_position(self):
        (i,j) = self.pos
        self.route[i].occ[j] = None
        
    ''' Return the car coordinates '''
    def get_coors(self):
        if self.arrivalTime > -1:
            return (-1,-1)
        (i,j) = self.pos
        if i == -1:
            return (i,j)
        orig = self.route[i].orig
        dest = self.route[i].dest
        x = orig.x + (float(j)/self.route[i].length)*(dest.x-orig.x)
        y = orig.y + (float(j)/self.route[i].length)*(dest.y-orig.y)
        ''' make the car ride on the right side of the street '''
        if orig.x == dest.x:
            ''' vertical line '''
            if dest.y > orig.y:
                ''' Going up'''
                x += 0.005
            else:
                ''' Going down '''
                x -= 0.005
        else:
            ''' Horizontal line '''
            if dest.x > orig.x:
                '''Going right'''
                y -= 0.005
            else:
                '''Going left '''
                y += 0.005
        return (x,y)
            
        