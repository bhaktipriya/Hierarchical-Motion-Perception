import numpy as np
from hierarchical_motion_mcmc import hierarchical_motion_mcmc
from defaults import set_defaults
from pos_gen import pos_gen

def simulator(pos,opts={}):
	timesteps=len(pos)
	objects=len(pos[0])
	print "Generating simulation for %d objects, with positions recorded for %d timesteps" %(objects, timesteps)
	R=hierarchical_motion_mcmc(pos,opts)	
	return R

def generate_positions(case):
	pos=[]
	if case==1:
		#Johansson's (1950) Experiment 19 with 2 dots
		t0=[[0,1], [1,0]]
		t1=[[0,0], [0,0]]
		pos=np.array([t0,t1])
	if case==2:
	 	#Johansson's (1950) 3 dot experiment
            	t0=[[0,0], [0,0.25], [0,1]]
            	t1=[[1,0], [1,0.75], [1,1]]
		pos=np.array([t0,t1])
	if case==3:
		n=20
		theta=np.pi/4.0
		R = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta),np.cos(theta)]])
		x=np.zeros((n,2,2))
		x[0] = np.array([[0,1],[0,0]])
		for i in range(1,n):
                	x[i,1] = x[i-1,1] + np.array([theta, 0])
                	x[i,0] = x[i,1] + np.dot(x[i-1,0]-x[i-1,1],R)
		pos=x
	return pos
	
pos=generate_positions(1)
opts=set_defaults({})
results=simulator(pos,opts)	
for k in results:
	if k=="score":
		print "SCORE=",results['score']
	if k=="parents":
		print results['parents']
	if k=="c" or k=="d":
		print k
		print results[k]
	if k=="opts":
		print np.shape(results['opts']['cov'])	
