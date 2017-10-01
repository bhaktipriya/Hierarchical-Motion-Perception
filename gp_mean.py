from gp_cov import gp_cov
from scipy.linalg import cho_solve
from scipy.linalg import cho_factor
from defaults import set_defaults
import numpy as np
def gp_mean(v,setnum,j,c,k,d,opts):
    
    #Posterior predictive mean for one component motion.
    #
    #USAGE: m = gp_mean(v,c,k,d,opts)
    v = v[setnum][j] #set 0 fixed limit to a given timestep
    n= np.shape(v)[0] #this gives num od timesteps
    #construct covariance matrix (excluding target function)
    K = gp_cov(opts['cov'][setnum][j],c,d)
    L = cho_factor(K/opts['s2']+np.eye(n))               #Cholesky factor of covariance with noise
    #construct target covariance matrix
    n = np.shape(K)[0]
    K0 = np.zeros((n,n))
    for i in range(n):
        if np.any(c[i,:d[i]]==k):
            for m in range(i,n):
                if np.any(c[m,:d[m]]==k):
                    K0[i][m] = opts['cov'][setnum][j][i][m]
                    K0[m][i] = opts['cov'][setnum][j][i][m]
    # compute predictive mean
    alpha = cho_solve(L,v)/opts['s2']
    m = np.dot(K0,alpha)
    return m
#TODO: unit test
#v=np.array([[[1.0000,0],[1.0000,0.5000],[1.0000,0]]])
#j=1-1#-1 req!
#c=np.array([[1,2,2],[1,3,4],[1,2,7]])-1
#k=2-1#-1 req!
#d=np.array([2,2,2])
#cov=np.array([[[[1.0000,0.9997,0.9950],[0.9997,1.0000,0.9972],[0.9950,0.9972,1.0000]]]])
#opts=set_defaults({'cov':cov})
#print gp_mean(v,j,c,k,d,opts)
