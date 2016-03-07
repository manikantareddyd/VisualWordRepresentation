from result import *
import pickle


for depth in [2,3,4]:
    for branches in [11]:
        r=result(s,branches,depth)
        p=r.finalResult
        print depth,branches,p[0],p[1][0],p[1][1],p[1][2],p[1][3]
        del p
        del r
        gc.collect()
