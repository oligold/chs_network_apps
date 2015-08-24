'''
Created on Aug 19, 2015

@author: olivier
Graph Utilities are a set of graph algorithms
'''
'''
    LeftRight determines the order of three points
'''
def  LeftRight(pt1,pt2,pt):
    if pt1.x == pt2.x:
        if ((pt.x < pt1.x and pt2.y < pt1.y) or (pt.x > pt1.x and pt2.y > pt1.y)):
            return True
        else:
            return False
    if pt1.y == pt2.y:
        if ((pt.y < pt1.y and pt1.x < pt2.x) or (pt.y > pt1.y and pt1.x > pt2.x)):
            return True
        else:
            return False
    a1= (pt1.y-pt2.y)/(pt1.x-pt2.x)
    b1= pt1.y - a1*pt1.x
    a2= (pt.y-b1)/a1
    if (((a2 < pt.x) and (pt1.y < pt2.y)) or ((a2 > pt.x) and (pt1.y > pt2.y))):
        return True
    else:
        return False

'''
Convex Hull returns a set of edges which form a convex envelope
of an Euclidean Graph
'''
def convexHull(g):
    nodes = g.get_nodes()
    if len(nodes) < 3:
        print 'Less than three nodes: no convex hull'
        return None
    convexOrder = [0] * len(nodes)
    tmpOrder = [0] * len(nodes)
    for key in nodes.keys():
        nodes[key].seen = False
    convexOrder[0] = 0
    convexOrder[1] = 1
    convexOrder[2] = 2
    if LeftRight(nodes[0], nodes[1], nodes[2]):
        convexOrder[1] = 2    
        convexOrder[2] = 1    
    convexSize = 3
    for i in range(3, len(nodes)):
        first = convexSize
        last = convexSize
        for j in range(convexSize):
            if j + 1 < convexSize:
                nexto = j + 1
            else:
                nexto = 0
          
            if LeftRight(nodes[convexOrder[j]],
                nodes[convexOrder[nexto]], nodes[i]):
                nodes[j].seen = False
            else:
                nodes[j].seen = True
        if nodes[0].seen:
            flag = True
        else:
            flag = False
        for j in range(convexSize):
            if not nodes[j].seen and flag:
                first = j
                flag = False
            if nodes[j].seen and not flag:
                last = j
                flag = True
        if first == convexSize and last < convexSize:
            first = 0
        if last == convexSize and first < convexSize:
            last = 0
        if not first == convexSize:
            tmpOrder[0] = i
            k = 1
            j = last
            while j != first:
                tmpOrder[k] = convexOrder[j]
                j += 1
                if j == convexSize:
                    j = 0
                k += 1
            tmpOrder[k] = convexOrder[j]
            convexSize = k + 1
            for k in range(convexSize):
                convexOrder[k] = tmpOrder[k]
    tmpOrder = []
    for ix in range(convexSize):
        tmpOrder.append(nodes[convexOrder[ix]])
    return tmpOrder
    
