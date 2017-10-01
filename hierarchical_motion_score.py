import numpy as np
from nCRP_treeprob import nCRP_treeprob
from defaults import set_defaults
from gp_lik import gp_lik
from sq_dist import sq_dist
def hierarchical_motion_score(x,c,parents,d,opts={}):
    timesteps,objects,dims=np.shape(x) 
    if not 'sets' in opts: #set numbering begins with 0
                opts['sets']=np.zeros(timesteps)        #put all in set 0
    S=set(opts['sets']) #unique
    v=np.zeros((len(S),timesteps-1,objects,dims))

    for s in S:
                ix=[ii for ii, xx in enumerate(opts['sets']) if xx == s]
                s=int(s)
                for j in range(len(ix)-1):#why -1?
                        v[s][j]=x[ix[j+1]]-x[ix[j]]#velocitY
                        opts['cov'][s][j]=opts['tau']*np.exp(-0.5*sq_dist(x[ix[j]].T)/opts['lambda'])
			#print opts['cov'][s][j]
    dd = (d==np.transpose(d)).astype(int)
    dd = np.sum(dd)
    #print gp_lik(v,c,d,opts)
	
    score = gp_lik(v,c,d,opts) + opts['alpha']*0.5*dd - opts['rho']*sum(d) + nCRP_treeprob(c,parents,opts['g'])
    return score

#Unit tested! :)
#c=np.array([[1,2,3],[1,2,5]])-1
#parents=np.array([0,1,2,1,4])-1
#d=[2,1]
#n = 20
#theta = np.pi/4;
#R = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta),np.cos(theta)]])
#x=np.zeros((n,2,2))
#x[0] = np.array([[0,1],[0,0]])
#cov=np.array([[1.0000,0.9950],[0.9950,1.0000]])
#cov=np.array([[cov]*19])
#print "cov shape", np.shape(cov)
#opts = set_defaults({})
#opts['cov']=cov
#for i in range(1,n):
#                x[i,1] = x[i-1,1] + np.array([theta, 0])
#                x[i,0] = x[i,1] + np.dot(x[i-1,0]-x[i-1,1],R)
            
		#print x[i]            
#print hierarchical_motion_score(x,c,parents,d,opts)
