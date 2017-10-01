import numpy as np
from scipy.special import gammaln
def nCRP_treeprob(c,parents,g,D=[]):
    
    # Evaluate probability of a tree under the nCRP.
    
    logp = 0
    if D ==[]:
	D=np.shape(c)[1]
    for d in range(D): # loop over levels
	u=[parents[i] for i in np.unique(c[:,d])] # set of parents for all customers at level d
        for j in u:
            ix=[c[i,d] for i in range(len(c)) if parents[c[i,d]]==j ] #set of children of parent j
            logp = logp + crp(ix,g)
    return logp
def crp(c,g):
    N = len(c)
    u = np.unique(c)
    K = len(u)
    logp = gammaln(g) + K*np.log(g) - gammaln(N+g)
    for k in u:
        logp = logp + gammaln(sum(c==k))
    return logp

#Unit tested! :)
#c=np.array([[1,2,3],[1,2,5]])-1
#parents=np.array([0,1,2,1,4])-1
#g=1
#print nCRP_treeprob(c,parents,g)
