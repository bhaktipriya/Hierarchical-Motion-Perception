import numpy as np
def fastrandsample(p):
	out=np.random.multinomial(1,p)
	for idx,val in enumerate(out):
		if val ==1:
		 	return idx
