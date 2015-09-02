'''
Created on Aug 16, 2015

@author: Mr Goldschmidt
'''

class Node:
    '''
    This class defines a node and its function
    '''


    def __init__(self, x,y):
        '''
        Constructor coordinates
        '''
        self.x = x
        self.y = y
        self.idx = -1
        self.color = 'lightgray'
        self.weight = -1
        self.seen = False
        self.neighs = []
        self.next = None