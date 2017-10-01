import numpy as np
def nCRP(c,parents,n,cn,g):

    #Log pdf for nested Chinese restaurant process.
    #
    #USAGE: logp = nCRP(c,parents,n,cn,g)

    c=np.delete(c, n, 0)
    logp = 0
	
    print cn	
    print parents	
    #loop over levels in the tree
    for j in range(len(cn)): #ignored level 0
        if cn[j]>=len(parents):
            break
	print "j=",j
        u = np.where(parents==parents[cn[j]])  #find all nodes that share common parent with proposed node
	u=u[0] #get indices only, np where returns a tuple where 2nd arg is not not req
	m = np.zeros(len(u))
        for k in range(len(u)):
            m[k] = np.sum(c[:,j]==u[k])       #collect occupancy counts
        a = m[u==cn[j]]                    #occupancy corresponding to proposed node
        #a+=1 #check
	if a == 0:                           #if the proposed node is unused
            a = g
            m[u==cn[j]] = g
        elif np.count_nonzero(m)==0:
            m+=[g]
        else:
            m[m==1] = g
            m[m==0] = g #check is this the best way to replace m[m==0 or m==1]
        m=m[m!=0]  #make sure we don't take log(0)
        logp = logp + np.log(a) - np.log(np.sum(m))
	assert np.size(logp)==1
    return logp
#unit testing check with without -1, 
#c=np.array([[1,4,5],[1,4,2],[1,2,3]])-1
#parents=np.array([0,1,2,1,4,1,6,5,5])-1
#n=2-1 #n-1
#cn=np.array([1,2,3])-1 #no -1 here
#g=2
#print nCRP(c,parents,n,cn,g)
