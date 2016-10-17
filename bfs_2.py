import numpy as np 
from problem_file import initial_states as init
from display import display2 as disp
from display import display3 as disp2
# state
class state_node:
	'base class for the each state, contains actions'
	total_node = 0
	def __init__(self, pre,board, indx):
		self.indx = indx
		self.pre = pre
		self.b = board
		state_node.total_node += 1
		
# actions

	def ver(self,n_obj,dir):
		xo = n_obj[1]
		yo = n_obj[0]
		if xo <0 or yo  < 0:
			return 0
		board = np.copy(self.b)
		obj_name = board[yo,xo]
		# find obj in same col
		y_arr = np.nonzero(board[:,xo]) # ------------------will give array of indices
		if dir == 'pos' :
			valid_pos = np.where(y_arr > yo)
		else:
			valid_pos = np.where(y_arr < yo)
		if  len(valid_pos[0]) > 1:
			
			if dir == 'pos':
				nearest_obj = np.amin(valid_pos[0])
				yo_new = nearest_obj-1
			else:
				nearest_obj = np.amax(valid_pos[0])
				yo_new = nearest_obj+1
			if yo_new == yo :
				return 0
			else :
				board[yo,xo] = 0
				board[yo_new,xo] = obj_name
				print 'object moved vert in dir' , dir
				return state_node(self.indx, board,state_node.total_node)
		else:
			return 0

	def hor(self,n_obj,dir):
		xo = n_obj[1]
		yo = n_obj[0]
		# if self.x[n_obj] <0 or self.y[n_obj] < 0:
		# 	return 0
		board = np.copy(self.b)
		obj_name = board[yo,xo]

		# find obj in same col
		x_arr = np.nonzero(board[yo]) # ------------------will give array of indices
		if dir == 'pos' :
			valid_pos = np.where(x_arr > xo)
		else:
			valid_pos = np.where(x_arr < xo)
		if  len(valid_pos[0]) > 1:
			if dir == 'pos':
				nearest_obj = np.amin(valid_pos)
				xo_new = nearest_obj-1
			else:
				nearest_obj = np.amax(valid_pos)
				xo_new = nearest_obj+1
			if xo_new == xo :
				return 0
			else :
				board[yo,xo] = 0
				board[yo,xo_new] = obj_name

				print 'object moved horizontally in dir' , dir
				return state_node(self.indx, board,state_node.total_node)
		else:
			return 0
	def expand(self,clist):
		temp_q = []			# temporary q for storing the bunh of nodes (~20) expanded from this node
		board = np.copy(self.b)
		for i in range(4):
			for j in range(4):
				if board[i,j] :
					new_node = self.hor([i,j],'pos')
					if new_node != 0 and not repeat_check(new_node, clist):
						temp_q.append(new_node)
						disp(new_node)
						
						
						
					new_node = self.hor([i,j],'neg')
					if new_node != 0 and not repeat_check(new_node, clist):
						temp_q.append(new_node)
						disp(new_node)
						
						
					new_node = self.ver([i,j],'pos')
					if new_node != 0 and not repeat_check(new_node, clist):
						temp_q.append(new_node)
						disp(new_node)
						

					new_node = self.ver([i,j],'neg')
					if new_node != 0 and not repeat_check(new_node, clist):
						temp_q.append(new_node)
						disp(new_node)
						

		return temp_q
def goal_check(q_check,goal):
	for i in range(len(q_check)):
		if q_check[i].x[-1] == goal[0] and q_check[i].y[-1] == goal[1]:
			return i
	return 0 
def backtrack(goal_node,clist):
	curr_br = goal_node.pre
	plan_tree = [goal_node]
	while curr_br !=0:
		plan_tree.append(clist[curr_br])
		curr_br = clist[curr_br].pre
	plan_tree.append(clist[0])
	return plan_tree

def repeat_check(node, clist):
	for i in range(len(clist)):
		curr_node = clist[i]
		if np.array_equal(node.b,curr_node.b):
			state_node.total_node -= 1
			return 1
	return 0		
def create_board(x,y):
	 board_temp = np.zeros([5,5],int)
	 for i in range(5):
	 	if (y[i] > -1) or (x[i] > -1):
	 		board_temp[y[i],x[i]] = 1
	 board_temp[y[5],x[5]] = 2
	 return board_temp
# ======================================================
#         START OF THE PLAN
#=======================================================

# for debug
x = np.array([1,2,3,4,4,2])
y = np.array([0,3,4,0,3,1])
init_board = create_board(x,y)
p_start = state_node(0,init_board,0)					# root node, having index 0
closed_list = [p_start]
list_nodes = p_start.expand(closed_list)

# reading input 
'''
init_states = init()
for i in range(len(init_states)):

	x = np.array(init_states[i][0])
	y = np.array(init_states[i][1])
	init_board = create_board(x,y)
	p_start = state_node(0,init_board,0)					# root node, having index 0

	# plan
	plan = [] 					# the final plan
	closed_list = []			# the node which have been opened up
	open_q = []					# the q of nodes which need to be exanded
	open_q.append(p_start)		# adding the root node
	while  open_q:
		exp_node = open_q[0]
		open_q.remove(open_q[0])
		closed_list.append(exp_node)
		print 'expanding state' , exp_node.indx
		# disp(exp_node)
		new_nodes_list = exp_node.expand(closed_list)
		check = goal_check(new_nodes_list,[2,2])
		if check != 0:
			print 'found goal'
			plan = plan + backtrack(new_nodes_list[check], closed_list)
			break
		else:
			open_q = open_q + new_nodes_list



	# printing the plan
	if len(plan) != 0:
		for i in range(len(plan)):
			disp(plan[-(i+1)])
			print '============='
	else:
		print 'no plan exist'
		print (len(closed_list))
		print len(open_q)
	raw_input('press enter to solve next game')
	state_node.total_node = 0

'''
