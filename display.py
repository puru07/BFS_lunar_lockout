import numpy as np
def display(node):
	 
	 disp = np.zeros([5,5],int)
	 for i in range(node.x.size):
	 	if (node.y[i] > -1) or (node.x[i] > -1):
	 		disp[node.y[i],node.x[i]] = i+1
	 print disp[4][:]
	 print disp[3][:]
	 print disp[2][:]
	 print disp[1][:]
	 print disp[0][:]

def display2(node):
	 disp = node.b
	 print disp[4,:]
	 print disp[3,:]
	 print disp[2,:]
	 print disp[1,:]
	 print disp[0,:]

def display3(node):
	 disp = node
	 print disp[4,:]
	 print disp[3,:]
	 print disp[2,:]
	 print disp[1,:]
	 print disp[0,:]
