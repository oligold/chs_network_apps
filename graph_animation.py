'''
Created on Aug 18, 2015

@author: olivier
Graph animation functions
'''
# import matplotlib
# matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


''' Animate function with no erasing '''
def animate_func(ix,g,edge_lsts,color):
    globalWidth = None
    if ix == len(edge_lsts)-1:
        color = 'blue'
        globalWidth = 1.5
    for (e,price) in edge_lsts[ix]:
        g.plot_edge(e,color,globalWidth)
        if ix < len(edge_lsts)-1:
            x,y = e.get_mid_point()
            txt = str(ix+1)+' - '+'%.2f' % price
            plt.text(x,y,txt,color=color, fontsize=9)
    return

''' Animate function for social graph evolution '''
def animate_func_evolv(ix,g,edge_lsts,color):
    g.plot_edge(edge_lsts[ix])
    return

''' Animate function for social graph evolution '''
def animate_func_car(ix,g,car_pos,color):
    g.draw()
    for (x,y) in car_pos[ix]:
        g.plot_point(x,y)
    return

''' Animate function with erasing '''
def animate_func_erase(ix,g,edge_lsts,color):
    globalWidth = 0.7
    (erase_lst,paint_lst) = edge_lsts[ix]
    for e in erase_lst:
        g.plot_edge(e,e.color,1)
    for e in paint_lst:
        g.plot_edge(e,color,globalWidth)
    return
'''
Animate algorithms: input is a list of set of edges at each step draw the 
edges from next set of edges
'''
def animate(g,edge_lsts,animate_function,msg,color='red',time_sleep=300,txtflag=False):
    fig = plt.figure()
    _anim = animation.FuncAnimation(fig, animate_function, frames=len(edge_lsts), 
                                   init_func=g.draw(None,None,txtflag), 
                                   fargs=(g,edge_lsts,color), 
                                   save_count=None, interval=time_sleep,repeat = False)
    if msg:
        plt.text(0,0,msg,color='black', fontsize=12)
    plt.show()
#     return anim

'''
Animate algorithms for cars: input is a list of set of edges at each step draw the 
edges from next set of edges
'''
def animate_car(g,car_pos_lsts,animate_function,msg,color='red',time_sleep=300,txtflag=False):
    fig = plt.figure()
    _anim = animation.FuncAnimation(fig, animate_function, frames=len(car_pos_lsts), 
                                   init_func=g.draw(None,None,txtflag), 
                                   fargs=(g,car_pos_lsts,color), 
                                   save_count=None, interval=time_sleep,repeat = False)
    if msg:
        plt.text(0,0,msg,color='black', fontsize=12)
    plt.show()
#     return anim
'''
Animate algorithms: input is a list of set of edges at each step draw the 
edges from next set of edges
'''
def create_movie(g,fname,edge_lsts,animate_function,msg,color='red',time_sleep=300,
                 txtflag=False, drawEdgesFlag = False):
    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=1, metadata=dict(artist='oligold'), bitrate=1800)

    fig = plt.figure()
    anim = animation.FuncAnimation(fig, animate_function, frames=len(edge_lsts), 
                                   init_func=g.draw(None,None,txtflag,drawEdgesFlag), 
                                   fargs=(g,edge_lsts,color),
                                   save_count=None, interval=time_sleep,repeat = False)
#     writer.grab_frame()
    if msg:
        plt.text(0,0,msg,color='black', fontsize=12)
    fname = 'results/%s.mp4' % fname
    anim.save(fname,writer = writer)
    # plt.show()
    return anim

'''
Animate algorithms: input is a list of set of edges at each step draw the 
edges from next set of edges
'''
def create_car_movie(g,fname,car_pos_lsts,animate_function,msg=None,color='red',time_sleep=1,
                 txtflag=False, drawEdgesFlag = False):
    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=1, metadata=dict(artist='oligold'), bitrate=1800)

    fig = plt.figure()
    anim = animation.FuncAnimation(fig, animate_function, frames=len(car_pos_lsts), 
                                   init_func=None, 
                                   fargs=(g,car_pos_lsts,color),
                                   save_count=None, interval=time_sleep,repeat = False)
#     writer.grab_frame()
    if msg:
        plt.text(0,0,msg,color='black', fontsize=12)
    fname = 'results/%s.mp4' % fname
    anim.save(fname,writer = writer)
    # plt.show()
    return anim
