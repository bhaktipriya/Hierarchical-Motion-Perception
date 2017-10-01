from nCRP_treeprob import nCRP_treeprob
def hierarchical_motion_score(x,c,parents,d,opts={})
    
    opts = set_defaults(opts)
    if not 'sets' in opts: #set numbering begins with 0
                opts['sets']=np.zeros(timesteps)        #put all in set 0
    S=set(opts['sets']) #unique

    for s in S:
                ix=[ii for ii, xx in enumerate(opts['sets']) if xx == s]
                s=int(s)
                for j in range(len(ix)-1):#why -1?
                        v[s][j]=x[ix[j+1]]-x[ix[j]]#velocitY
                        opts['cov'][s][j]=opts['tau']*np.exp(-0.5*np.linalg.norm(x[ix[j]])/opts['lambda'])

    
    dd = (d==np.transposed(d)).astype(int)
    dd = np.sum(dd(:))
    score = gp_lik(v,c,d,opts) + opts['alpha']*0.5*dd - opts['rho']*sum(d) + nCRP_treeprob(c,parents,opts.g)
    return score
