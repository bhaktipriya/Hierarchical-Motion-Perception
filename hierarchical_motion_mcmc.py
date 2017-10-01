import numpy as np
import copy
from nCRP_sample import nCRP_sample
from enumerate_paths import enumerate_paths
from gp_lik import gp_lik
from gp_mean import gp_mean
from nCRP import nCRP
from scipy.misc import logsumexp
from fastrandsample import fastrandsample
from active_nodes import active_nodes
from sq_dist import sq_dist
from hierarchical_motion_score import hierarchical_motion_score
def hierarchical_motion_mcmc(x,opts,results={}):
	timesteps,objects,dims=np.shape(x)
	print "Tsprets", timesteps
	N = objects
	sets=[]
	if not 'sets' in opts: #set numbering begins with 0
		opts['sets']=np.zeros(timesteps)	#put all in set 0
	S=set(opts['sets']) #unique
	if not 'cov' in opts:
		opts['cov']=np.zeros((len(S),timesteps-1,objects,objects))#check if its okay to initialize it with zeroes,init to timesteps-1(that's the conv followed
	v=np.zeros((len(S),timesteps-1,objects,dims))
		
	for s in S:
		ix=[ii for ii, xx in enumerate(opts['sets']) if xx == s]
		s=int(s)	
		for j in range(len(ix)-1):#why -1?
			v[s][j]=x[ix[j+1]]-x[ix[j]]#velocitY
			opts['cov'][s][j]=opts['tau']*np.exp(-0.5*sq_dist(x[ix[j]].T)/opts['lambda'])

	d=np.zeros(objects)
	c=np.zeros((objects,opts['d_max']))
	parents=[]
	if results=={}:
		d=np.zeros((objects))+opts['d0']
		c, parents = nCRP_sample(objects,opts);
	else:
		c=results['c']
		d=results['d']
		parents=results['parents']
	c=c.astype(int)
	d=d.astype(int)
	dd=copy.deepcopy(d)
	parents=parents.astype(int)
	for i in xrange(opts['nIter']):
		print "Iteration:", i
		# annealing temperature
        	bt = 2/np.log(1.00000000001+i)

		# update cluster assignments (gibbs sampling)
        	for n in np.random.permutation(N):
			#print "ENUM"
			#print c
			#print parents
			#print d
			#print n
			#print "ENUM"
            		C = enumerate_paths(c,parents,d,n,opts)
            		logp = np.zeros((len(C)))
            		for t in xrange(len(C)):
                		c1 = copy.deepcopy(c)
                		c1[n][:d[n]] = copy.deepcopy(C[t])
				
                		logp[t] = gp_lik(v,c1,d,opts) + nCRP(c1,parents,n,C[t],opts['g']) 
            	logp = logp/bt
            	p = np.exp(logp-logsumexp(logp))
            	c[n][:d[n]] = copy.deepcopy(C[fastrandsample(p)])

            	#add new parents if necessary
            	for j in range(1,d[n]): 
                	if c[n][j]>=len(parents):
				#print parents, c[n][j]
                    		parents=np.append(parents,c[n][j-1])

                #update depth allocations (gibbs sampling)
        	if opts['update_depth']==1:
            		for n in np.random.permutation(N):
                		logp = np.zeros(opts['d_max'])
                		dn = copy.deepcopy(d)
                		ix = np.arange(N)!=n
                		for j in range(opts['d_max']):
                    			dn[n] = j+1 #dont want 0 depth
                    			logp[j] = gp_lik(v,c,dn,opts) + opts['alpha']*np.sum(d[ix]==j) - opts['rho']*j
                		logp = logp/bt
                		p = np.exp(logp-logsumexp(logp))
                		d[n] = fastrandsample(p)+1	

	results['c'] = c
        results['d'] = d
        results['opts'] = opts
        
	setnum=0 #assume setnum is 0
	k_active = active_nodes(c,d)
	num_active = len(k_active)
	#print "vsahpe", np.shape(v[setnum])

	tsteps,obj,dims = np.shape(v[setnum])
	#m={}
    	#for ki in range(len(k_active)):
        #	for j in range(len(v[setnum])): #assume set is 0
        #    		m[(ki,j)] = gp_mean(v,setnum,j,c,k_active[ki],d,opts)#j, k may req -1 #this is the only call to gp_mean and takes set as 0 by default
        results['score'] = hierarchical_motion_score(x,c,parents,d,opts);
    	results['k_active'] = k_active
    	#results['m'] = m
    	results['c'] = c
    	results['d'] = d
    	results['parents'] = parents
    	results['opts'] = opts
    	results['v']=v
	return results    
