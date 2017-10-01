import numpy as np
from fastrandsample import fastrandsample
from defaults import set_defaults

#a=[1-1,2-1,2-1,2-1,1-1,3-1]
#ctx=0

def nCRP_sample(N,opts):

    #Draw random samples from the nested CRP.
    #
    #USAGE: c, parents = nCRP_sample(N,opts)
    #
    # INPUTS:
    #   N - number of objects
    #   opts - options structure
    #
    # OUTPUTS:
    #   c - [N x opts.d_max] matrix of paths
    #   parents - [1 x max(c(:))] vector of parents for nodes in the tree

    #code follows indexing from 0, as done in matlab
    #As in objects are labelled as 0,1,2,3 ... path for obj0 is at c[0]
    opts=set_defaults(opts)
    c = np.zeros((N,opts['d_max']))
    c.fill(-1)
    c[:,0] = 0 #motion component 1
    parents = [-1] #list
    for n in range(N):
        for j in range(1,opts['d_max']):
            #print c
	    #print "n=", n, "j=", j	
            p = c[n,j-1]
	    #print p,
            u = []  #find all nodes(mc's) that share common p #list
	    for idx,val in enumerate(parents):
			if val==p:
				u+=[idx]
	    #print parents,
            if len(u)==0:
                c[n,j] = np.max(c)+1                #make a new node if none exist at this level
            else:
                m = [0]*(len(u)+1) 
		m[-1]=opts['g']
                for k in range(len(u)):
                    m[k] = np.sum(c[:,j]==u[k])       #collect occupancy counts
                ix = fastrandsample(m/sum(m))
		#ctx+=1
		#print "===="
		#print n
		#print "....."
		#print j
		#print "---"
		#print u
                if ix >= len(u):
                    c[n,j] = np.max(c)+1           #make a new node
                else:
                    c[n,j] = u[ix]                 #reuse old node
	#	print "non empty"
                
            
	    if c[n,j] >= len(parents):  #new component added. Add it's parent
                parents+=[p]
    parents=np.array(parents)
    print c
    print parents
    print np.max(c), (np.size(parents)-1)
    assert np.max(c)==(np.size(parents)-1)
    return (c,parents)

#c,par=nCRP_sample(5,{})
