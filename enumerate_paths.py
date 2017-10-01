from defaults import set_defaults
from active_nodes import active_nodes
import numpy as np
def enumerate_paths(c,parents,d,n,opts):
    #Enumerate all possible paths for a single datapoint.

    objts,maxdepth=np.shape(c)
    k_active = active_nodes(c,d)
    opts['K_max'] = 10*opts['d_max']*objts
    k_inactive = np.setdiff1d(range(opts['K_max']),k_active); #indices for inactive nodes
    C = [[]]*len(k_active)
    count = np.zeros(len(k_active))
    result=[]	
    for i in range(len(k_active)):
        f = int(k_active[i])
	print f
        C[i] = [f]
        f = parents[f]
        while f!=-1: #watch out, indexing begins with 0 here, set parent of 0 to -1?
	    #print "	f=",f,C[i]
            C[i]=[f]+C[i]
            f = parents[f]
	
	end=max(d[n]-len(C[i]),0)
        C[i] += k_inactive[:end].tolist()    #add new nodes for paths terminating on internal nodes
        count[i] = len(C[i])
	#print C[i]
	if count[i]>d[n]:
		C[i]=[]#remove paths that are too deep
	else:
		result.append(C[i])
    result=np.array(result)
    return result

#very well unite tested. Can't be wrong for sure
#c=np.array([[1,4,4],[1,2,3],[1,3,8]])-1
#parents=np.array([0 ,    1,     2,     1,     4,     1,6,5,5    ])-1
#d=np.array([2,0,2]) #this was 2 earlier. check -1
#n=2
#opts=set_defaults()
#print enumerate_paths(c,parents,d,n,opts)+1

#c=np.array([[1,4,2],[1,3,8],[1,6,7]])-1
#parents=np.array([0,1,2,1,4,1,6])-1
#d=np.array([1,2,1])
#n=0
#opts=set_defaults()
#print enumerate_paths(c,parents,d,n,opts)+1

#This case will throw error becuase c is incorretly constructed
#c=np.array([[0,2 ,7],[0, 2 ,7],[0, 3 ,6]])
#parents=np.array([-1 , 0 , 1 , 0 , 3 , 0 , 5])
#d=np.array([3,2,1])
#n=1
#opts=set_defaults()
#print enumerate_paths(c,parents,d,n,opts)+1


