import numpy as np
def active_nodes(c,d):
    #find which nodes are active
    #nodes which occur on the paths of the objects	
    objects, maxdep=np.shape(c)
    k_active=np.array([])
    for o in range(objects):
    	obj_act=np.unique(c[o,:d[o]])
	k_active=np.append(k_active,obj_act)
    k_active=np.unique(k_active)
    return k_active

