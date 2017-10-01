from gp_cov import gp_cov
from scipy.linalg import cho_solve
from scipy.linalg import cho_factor
from defaults import set_defaults
import numpy as np
import math
def gp_lik(v,c,d,opts):

    #Log-likelihood function for Gaussian process layered motion model
    
    # USAGE: lik = gp_lik(v,c,d,opts)

    sets,tsteps,objs,dims=np.shape(v)
	
    lik = 0;
    #compute likelihood
    for s in range(sets):
        for i in range(tsteps):
            if np.size(v[s][i]): #check if this cell is occupied
                K = gp_cov(opts['cov'][s][i],c,d)
                L = cho_factor(K+opts['s2']*np.eye(objs))               #Cholesky factor of covariance with noise
		alpha = cho_solve(L,v[s][i])
                L=L[0]#knock out the boolean
		#print opts['cov'][s][i]
                lik = lik - np.dot(v[s,i].flatten(),(alpha.flatten()/2)) - np.sum(np.log(np.diag(L))) - 0.5*objs*np.log(2*np.pi*opts['s2']) #log marginal likelihood
    return lik
#exactly same, no 0-1 scaling done
#v=np.array([[[[0,-1],[-1,0]]]])
#c=np.array([[1,6,7],[1,2,6]])
#d=np.array([3,3])
#cov=np.array([[[[1.0000,0.9608],[0.9608,1.0000]]]])
#opts=set_defaults({'s2':0.0100, 'cov':cov})
#print gp_lik(v,c,d,opts)
