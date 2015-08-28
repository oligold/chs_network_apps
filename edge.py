'''
Created on Aug 16, 2015

@author: olivier
'''
import math

class Edge:
    '''
    This class defines an edge and its functions
    '''


    def __init__(self, orig, dest):
        '''
        Constructor orig and dest are the endpoints of the edge
        '''
        self.orig = orig
        self.dest = dest
        self.color = 'lightgray'
        self.width = 1
        self.length = 0
        self.qual = -1 
    
    ''' Return the vertex that is the other endpoint of the edge '''
    def get_other_vertex(self,nd):
        if self.orig == nd:
            return self.dest
        else:
            return self.orig

    ''' return the midpoint of the edge '''
    def get_mid_point(self):
        distx = math.fabs(self.orig.x-self.dest.x)/2
        disty = math.fabs(self.orig.y-self.dest.y)/2
        basex = min(self.orig.x,self.dest.x)
        basey = min(self.orig.y,self.dest.y)
        return basex+distx, basey+disty
        