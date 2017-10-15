import numpy as np
from copy import deepcopy
def gp_cov(K0,c,d):
    #Evaluate covariance matrix for Gaussian process layered motion model.
    #K [objects][x,y]
    #USAGE: K = gp_cov(K,c,d)
    #print "args for gp_cov"
    #print "#############"
    #print K0
    #print c
    #print d
    #print "#############"
    assert len(np.shape(K0))==2
    c=c.astype(float)
    tsteps= np.shape(K0)[0]
    K = np.zeros(tsteps)
    for i in range(np.max(d)):
        q=deepcopy(c[:,i]) #all nodes at depth i
	for idx,val in enumerate(d):
		if (val)<(i+1):
        		q[idx]=-1
        		c[idx,i]=np.nan
	p=np.atleast_2d(c[:,i])
	q=np.atleast_2d(q)
	#print "~~~~~~~~~~~~~~~~~~"
	#print c[:,i]+1
	#print "%%%%%%%%%%%%%%%%%%%"
	#print q.T+1
	#print "%%%%%%%%%%%%%%%%%%%"
	#print  (p.T==q).astype(int)
	#print "~~~~~~~~~~~~~~~~~~"

        K = K + (p==q.T).astype(int)
    K = K*K0
    #print K
    return K
#K0=np.array([[1.0000, 0.9950],[0.9950,1.0000]])
#c=np.array([ [1.0,2.0,3.0],[1.0,2.0,5.0]])-1
#d=np.array([2,1]) #check dims
#DONE : unit test
#K0=np.array([[1.0000,0.9997,0.9950],[0.9997,1.0000,0.9972],[0.9950,0.9972,1.0000]])
#c=np.array([ [1.0,2.0,2.0],[1.0,2.0,3.0],[1.0,4.0,3.0]])-1
#d=np.array([1,3,1]) #check dims
#print gp_cov(K0,c,d)
