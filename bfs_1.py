import numpy as np 
from display import display as disp
from problem_file import initial_states as init
# state
class state_node:
	'base class for the each state, contains actions'
	total_node = 0
	def __init__(self, pre,x,y, indx):
		self.indx = indx
		self.pre = pre
		self.x = x
		self.y = y
		state_node.total_node += 1
		
# actions

	def ver(self,n_obj,dir):
		if self.x[n_obj] <0 or self.y[n_obj] < 0:
			return 0
		xo = self.x[n_obj]
		x_arr = self.x
		y_arr = self.y
		# find obj in same col

		same_col_obj = np.where(x_arr == xo)		# obj indx in same col, or same x value

		rows = y_arr[same_col_obj]						# rows (vertical val) of players in same col

		if dir == 'pos' :
			valid_row = rows[np.where(y_arr[n_obj]<rows)]		# y position of players above our player
		else:
			valid_row = rows[np.where(y_arr[n_obj]>rows)]		# y position of players above our player
		if valid_row.size != 0 :
			if dir == 'pos':
				nearest_obj = np.amin(valid_row)
				yo_new = nearest_obj-1
			else:
				nearest_obj = np.amax(valid_row)
				yo_new = nearest_obj+1
			
			if yo_new == y_arr[n_obj] :
				return 0
			else :
				y_arr_new = np.copy(self.y)
				y_arr_new[n_obj] = yo_new
				return state_node(self.indx, self.x,y_arr_new,state_node.total_node)
		else:
			return 0

	def hor(self,n_obj,dir):
		if self.x[n_obj] <0 or self.y[n_obj] < 0:
			return 0
		x_arr = self.x
		yo = self.y[n_obj]
		# find obj in same col
		same_row_obj = np.where(self.y == yo)
		cols = x_arr[same_row_obj]
		if dir == 'pos' :
			valid_row = cols[np.where(x_arr[n_obj]<cols)]
		else:
			valid_row = cols[np.where(x_arr[n_obj]>cols)]
		if valid_row.size != 0 :
			if dir == 'pos':
				nearest_obj = np.amin(valid_row)
				xo_new = nearest_obj-1
			else:
				nearest_obj = np.amax(valid_row)
				xo_new = nearest_obj+1
			if xo_new == x_arr[n_obj] :
				return 0
			else :
				x_arr_new = np.copy(self.x)
				x_arr_new[n_obj] = xo_new
				return state_node(self.indx, x_arr_new,self.y,state_node.total_node)
		else:
			return 0
	def expand(self,clist):
		temp_q = []			# temporary q for storing the bunh of nodes (~20) expanded from this node
		for i in range(self.x.size):
			

			new_node = self.ver(i,'pos')
			if new_node != 0:
				if not repeat_check(new_node,clist):
					temp_q.append(new_node)
			new_node = self.ver(i,'neg')
			if new_node != 0:
				if not repeat_check(new_node,clist):
					temp_q.append(new_node)
			
			new_node = self.hor(i,'pos')
			if new_node != 0:
				if not repeat_check(new_node,clist):
					temp_q.append(new_node)
			new_node = self.hor(i,'neg')
			if new_node != 0:
				if not repeat_check(new_node,clist):
					temp_q.append(new_node)

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
		if np.array_equal(node.x,curr_node.x) and np.array_equal(node.y,curr_node.y):
			state_node.total_node -= 1
			return 1

	return 0		

# ======================================================
#         START OF THE PLAN
#=======================================================

# reading input 
init_states = init()
for i in range(len(init_states)):

	x = np.array(init_states[i][0])
	y = np.array(init_states[i][1])
	p_start = state_node(0,x,y,0)					# root node, having index 0

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
		print 'the length of the plan is ', len(plan)
	else:
		print 'no plan exist'
		print (len(closed_list))
		print len(open_q)
	raw_input('press enter to solve next game')
	state_node.total_node = 0


