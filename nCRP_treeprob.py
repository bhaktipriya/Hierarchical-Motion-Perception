from scipy.special import gammaln
def nCRP_treeprob(c,parents,g,D=[]):
    
    # Evaluate probability of a tree under the nCRP.
    
    logp = 0
    if D ==[]:
	D=np.shape(c)[1]
    for d in range(D): # loop over levels
        u = parents(unique(c(:,d))');   # set of parents for all customers at level d
        for j in u:
            ix = parents(c(:,d)) == j;  % set of children of parent j
            logp = logp + crp(c(ix,d)',g);
        end
    end
    
end

def crp(c,g)
    N = len(c)
    u = np.unique(c)
    K = len(u)
    logp = gammaln(g) + K*log(g) - gammaln(N+g)
    for k in u:
        logp = logp + gammaln(sum(c==k))
    return logp
