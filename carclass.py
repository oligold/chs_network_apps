'''
Created on Sep 13, 2015

@author: olivier
'''
from matplotlib.font_manager import path

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
        ''' Position of the car as road and position on road '''
        self.pos = (-1,-1)
        self.idx = -1
        self.stopped = True
    
    def get_next_pos(self):
        ''' return car next position '''
        (i,j) = self.pos
        if j < self.route[i].length-1:
            return (i,j+1)
        elif i < len(self.route)-1:
            return (i+1,0)
        else:
            ''' Car has arrived at destination '''
            return (-1,-1)
    ''' Move the car '''    
    def move_car(self):
        self.free_current_position()
        (i,j) = self.get_next_pos()
        self.route[i].occ[j] = self
        
    ''' Free current position '''   
    def free_current_position(self):
        (i,j) = self.pos
        self.route[i].occ[j] = None
        
    ''' Return the car coordinates '''
    def get_coors(self):
        (i,j) = self.pos
        if i == -1:
            return (i,j)
        orig = self.route[i].orig
        dest = self.route[i].dest
        x = orig.x + (float(j)/self.route[i].length)*(dest.x-orig.x)
        y = orig.y + (float(j)/self.route[i].length)*(dest.y-orig.y)
        return (x,y)
            
        