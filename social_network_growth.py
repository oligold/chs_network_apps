'''
Created on Aug 26, 2015

@author: olivier
'''

import random

'''
    Social networks grow by adding strong and weak links.  Also new links are created
    by the law of triadic closure: If B and C are connected to A, then
    1. if both (A,B) and (A,C) are strong links, then (B,C) will be connected by 
        triadic closure with strong link with probability pss and weak link with
        probability (1-pss)
    2. if one of the link is weak and the other is strong, then (B,C) will be connected
        by a weak link (or strong link if B and C are close enough)
         with probability psw and not connected with probability (1-psw).
    3. if both links are weak, then (B,C) are connected by a weak link (or strong link 
        if B and C are close enough) with probability pww and not connected with
        probability (1-pww)
'''

'''
    Growing rules:
        1. At every step, one selects a new link randomly among possible strong or 
            weak links, say (A,B).
        2. After adding the link, one checks all neighbors of A (not B) and all 
            neighbors of B (not A) and use triadic rules to add triadic links
    Parameters:
        gr   = complete graph with nodes in the unit square
        stlk = maximum distance between two nodes to form a strong link
        wklk = maximum distance between two nodes to form a weak link
        pss = probability that the link between two strong neighbors of a node is
                itself a strong link
        psw = probability that a strong and weak neighbor of a node create a triadic link
        pww = probability that two weak neighbors of a node create a triadic link.
'''
def grow_social_network(gr,stlk = 0.03, wklk = 0.1, pss = 0.3, psw = 0.5, pww = 0.1):
    ''' Create a list with all links which are potential strong or weak links '''
    potentialLkLst = []
    for e in gr.get_edges():
        if e.length < wklk:
            potentialLkLst.append(e)
    while len(potentialLkLst) > 0:
        ''' Select a random link in the pool of potential links '''
        ix = int(random.random()*len(potentialLkLst))
        select_e = potentialLkLst.pop(ix)
        ''' Determine if link is strong or weak '''
        if select_e.length <stlk:
            select_e.qual = 1
            select_e.color = 'red'
        else:
            select_e.qual = 0
            select_e.color = 'black'
        ''' Add adjacencies to link node '''
        select_e.orig.neighs.append(select_e)
        select_e.dest.neighs.append(select_e)
        potentialLkLst = compute_triadic_closures(gr,potentialLkLst,[],pss,psw,pww)
        
def compute_triadic_closures(gr,potentialLkLst,addedLkLst,pss,psw,pww):
    ''' Compute all the new triadic links triggered by the new link '''
    while len(addedLkLst) > 0:
        ''' Extract next added link '''
        lk = addedLkLst.pop()
        
    
