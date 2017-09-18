import numpy as np
from hierarchical_motion_mcmc import hierarchical_motion_mcmc

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

	return pos
	
pos=generate_positions(2)
results=simulator(pos,{})		
