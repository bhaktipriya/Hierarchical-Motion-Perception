import numpy as np
def gp_cov(K0,c,d):
    #Evaluate covariance matrix for Gaussian process layered motion model.
    #K [objects][x,y]
    #USAGE: K = gp_cov(K,c,d)
    #print "args for gp_cov"
    #print K0
    #print c
    #print d
    assert len(np.shape(K0))==2
    c=c.astype(float)
    tsteps= np.shape(K0)[0]
    K = np.zeros(tsteps)
    for i in range(np.max(d)):
        p=c[:,i] #all nodes at depth i
        q=c[:,i] #all nodes at depth i
        q[d<(i+1)]=0
        c[d<(i+1),i]=np.nan
	q=q.reshape(q.shape + (1,))
	p=p.reshape(p.shape + (1,))
        K = K + (p==np.transpose(q)).astype(int)
    K = K*K0
    return K
#K0=np.array([[33.0000,3.3208],[2.9608,32.0000]])
#c=np.array([ [1.0,3.0,4.0],[1.0,2.0,4.0]])
#d=np.array([3,3]) #check dims
#DONE : unit test
#K0=np.array([[1.0000,0.9997,0.9950],[0.9997,1.0000,0.9972],[0.9950,0.9972,1.0000]])
#c=np.array([ [1.0,2.0,2.0],[1.0,2.0,3.0],[1.0,4.0,3.0]])-1
#d=np.array([1,3,1]) #check dims
#print gp_cov(K0,c,d)
