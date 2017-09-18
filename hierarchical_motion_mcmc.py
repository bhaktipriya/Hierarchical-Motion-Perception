def hierarchical_motion_mcmc(x,opts,results):
	timesteps=len(x)
        objects=len(x[0])

	sets=[]
	if not 'sets' in opts:
		opts['sets']=np.ones(timesteps)	
	if not 'cov' in opts:
		opts['cov']={}
	S=set(opts['sets']) #unique
	v={}
		
	for s in S:
		ix=[i for i, x in enumerate(opts['sets']) if x == s]
		for j in len(ix)-1:
			if s not in v:
				v[s]={}
			v[s][j]=x[ix[j+1]]-x[ix[j]]#velocity
			opts['cov'][s][j]=opts['tau']*np.exp(-0.5*sq_dist(x[ix[j]])/opts.lambda)

	d=[]
	c=[]
	parents=[]
	if results==[]:
		d=np.zeros((objects,1))+opts['d0']
		c, parents = nCRP_sample(objects,opts);
	else:
		c=results['c']
		d=results['d']
		parents=results['parents']
	
	for i in xrange(opts['nIter']):
		print "Iteration:", i
		# annealing temperature
        	bt = 2/np.log(1+i);

		# update cluster assignments (gibbs sampling)
        	for n in randperm(N):
            		C = enumerate_paths(c,parents,d,n,opts);
            		logp = np.zeros(1,len(C))
            		for t in xrange(len(C)):
                		c1 = c
                		c1[n][:d[n]] = C[t]
                		logp[t] = gp_lik(v,c1,d,opts) + nCRP(c1,parents,n,C[t],opts['g'])
            logp = logp/bt;
            p = np.exp(logp-logsumexp(logp,2))
            c[n][:d[n]] = C[fastrandsample(p)]

            #add new parents if necessary
            for j in range(1, d[n]):
                if c[n][j]>len(parents):
                    parents[c[n][j]] = c[n][j-1];



	
