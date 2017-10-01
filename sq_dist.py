import numpy as np
def sq_dist(A, B=None):
    """
    Calculate the squared-distance sq_dist(x,x') = (x-x')^2. If only
    one argument is supplied, then it's just sq_dist(x,x).
    """
    D, n = A.shape
    if B is None:
        mu = np.atleast_2d(np.mean(A, axis=1))
        a = A-np.tile(mu.T,(1,A.shape[1]))
        b = a
        m = n
    else:
        d, m = B.shape
        if d is not D:
            raise ValueError("sq_dist(): Both matrices must have same"
                             "number of columns.")
        mu = (m/(n+m))*np.mean(B, axis=1) + (n/(n+m))*np.mean(A, axis=1)
        a = A-np.tile(mu, (1,n))
        b = B-np.tile(mu, (1,m))
    C=np.sum(np.multiply(a,a).T,1)+np.sum(np.multiply(b,b).T,1)-2*np.dot(a.T,b)
    # Make sure we're staying positive :)
    C = C.clip(min=0)
    return C
#UNIT TESTED
#a=np.array([[ 3234.4342,  3245.33],[ 65.4534,  3267.543 ]])
#print sq_dist(a)
