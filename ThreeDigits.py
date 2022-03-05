import sys

#https://stackoverflow.com/questions/59450983/making-all-numbers-in-a-list-3-digit-numbers
def ditgitConvert(num):
    '''
    Adds leading 0s to numbers with < 3 digits, and returns as string
    '''
    if len(str(num))<3:
        num = '0'*(3-len(str(num)))+str(num)
    return str(num)

def get_heuristic(state_a, state_b):
	return abs(int(state_a[0]) - int(state_b[0])) + abs(int(state_a[1]) - int(state_b[1])) + abs(int(state_a[2]) - int(state_b[2]))

class node:
	def __init__(self, value, parent, depth, prev_change):
		self.value = value
		self.parent = parent
		self.depth = depth
		self.prev_change = prev_change

	def child_opt(self, forb):
		child = []
		if int(self.value) > 99 and self.prev_change != 3:
			if ditgitConvert(int(self.value) - 100) not in forb:
				child.append(node(ditgitConvert(int(self.value) - 100), self, self.depth + 1, 3))
		if int(self.value) < 900 and self.prev_change != 3:
			if ditgitConvert(int(self.value) + 100) not in forb:
				child.append(node(ditgitConvert(int(self.value) + 100), self, self.depth + 1, 3))
		if int(self.value[1:]) > 9 and self.prev_change != 2:
			if ditgitConvert(int(self.value) - 10) not in forb:
				child.append(node(ditgitConvert(int(self.value) - 10), self, self.depth + 1, 2))
		if int(self.value[1:]) < 90 and self.prev_change != 2:
			if ditgitConvert(int(self.value) + 10) not in forb:
				child.append(node(ditgitConvert(int(self.value) + 10), self, self.depth + 1, 2))
		if int(self.value[2:]) > 0 and self.prev_change != 1:
			if ditgitConvert(int(self.value) - 1) not in forb:
				child.append(node(ditgitConvert(int(self.value) - 1), self, self.depth + 1, 1))
		if int(self.value[2:]) < 9 and self.prev_change != 1:
			if ditgitConvert(int(self.value) + 1) not in forb:
				child.append(node(ditgitConvert(int(self.value) + 1), self, self.depth + 1, 1))
		return child

def bfs(start, end, forb):
	root = node(start, None, 0, 0)
	queue = []
	expanded = []
	queue.append(root)
	while len(queue) > 0:
		current = queue.pop(0)
		exi = False
		for x in expanded:
			if (x.value == current.value) and (x.prev_change == current.prev_change):
				exi = True
				break;
		if exi == False:
			expanded.append(current)
			child = current.child_opt(forb)
			#Found the goal node
			if current.value == end:
				break
			for x in child:
				queue.append(x)
		if len(expanded) > 1000:
			print("No solution found")
			second_line = []
			for x in expanded:
				second_line.append(x.value)
			print(",".join(second_line))
			return

	first_line = []
	first_line.append(end)
	while current.parent != None:
		first_line.append(current.parent.value)
		# print(current.parent.value, "1st")
		current = current.parent
	first_line.reverse()
	print(",".join(first_line))
	# print(len(expanded), "len")
	second_line = []
	for x in expanded:
		second_line.append(x.value)
	print(",".join(second_line))
	# print(second_line)

def dfs(start, end, forb):
	root = node(start, None, 0, 0)
	fringe = []
	expanded = []
	found_flag = False
	fringe.append(root)
	while len(fringe) > 0 and len(expanded) < 1000:
		current = fringe.pop(0)
		expanded.append(current)
		if current.value == end:
			found_flag = True
			break
		child = current.child_opt(forb)
		child.reverse()
		for x in child:
			exi = False
			for y in expanded:
				if (x.value == y.value) and (x.prev_change == y.prev_change):
					exi = True
					break
			if exi == False:
				fringe.insert(0, x)

	if found_flag == True:
		first_line = []
		first_line.append(end)
		while current.parent != None:
			first_line.append(current.parent.value)
			# print(current.parent.value, "1st")
			current = current.parent
		first_line.reverse()
		print(",".join(first_line))
	else:
		print("No solution found")
	second_line = []
	for x in expanded:
		second_line.append(x.value)
	print(",".join(second_line))
	# print(len(expanded), "len")

def ids(start, end, forb):

	root = node(start, None, 0, 0)
	expanded = []
	found_flag = False
	d = 0
	# fringe.append(root)

	while found_flag == False and len(expanded) < 1000:
		current_expanded = []
		fringe = []
		fringe.append(root)

		while len(fringe) > 0 and ((len(expanded) + len(current_expanded)) < 1000) and found_flag == False:
			current = fringe.pop(0)

			exi = False
			for x in current_expanded:
				if (x.value == current.value) and (x.prev_change == current.prev_change):
					exi = True
					break
			if exi == False:

				current_expanded.append(current)

				if current.value == end:
					found_flag = True
					break;

				if current.depth < d:
					child = current.child_opt(forb)
					child.reverse()
					for x in child:
						exi = False
						for y in current_expanded:
							if (x.value == y.value) and (x.prev_change == y.prev_change):
								exi = True
								break
						if exi == False:
							fringe.insert(0,x)

		for x in current_expanded:
			expanded.append(x)

		if found_flag == True:
			break
		else:
			d += 1

	if found_flag == True:
		first_line = []
		first_line.append(end)
		while current.parent != None:
			first_line.append(current.parent.value)
			current = current.parent
		first_line.reverse()
		print(",".join(first_line))
	else:
		print("No solution found")
	second_line = []
	for x in expanded:
		second_line.append(x.value)
	print(",".join(second_line))
	# print(len(expanded), "len")

def greedy(start, end, forb):

	root = node(start, None, 0, 0)
	fringe = []
	expanded = []
	found_flag = False

	fringe.append(root)

	while found_flag == False and len(expanded) < 1000 and len(fringe) > 0:
		current = fringe.pop(0)
		expanded.append(current)

		if current.value == end:
			found_flag = True
			break

		child = current.child_opt(forb)
		for x in child:
			exi = False
			for z in expanded:
				if (z.value == x.value) and (z.prev_change == x.prev_change):
					exi = True
					break
			if exi == False:
				idx = 0
				for y in fringe:
					if get_heuristic(y.value, end_state) >= get_heuristic(x.value, end_state):
						break
					idx += 1
				fringe.insert(idx, x)

	if found_flag == True:
		first_line = []
		first_line.append(end)
		while current.parent != None:
			first_line.append(current.parent.value)
			current = current.parent
		first_line.reverse()
		print(",".join(first_line))
	else:
		print("No solution found")
	second_line = []
	for x in expanded:
		second_line.append(x.value)
	print(",".join(second_line))

def hill(start, end, forb):
	root = node(start, None, 0, 0)
	expanded = []
	found_flag = False
	current = root

	while len(expanded) < 1000 and found_flag == False:
		expanded.append(current)
		if current.value == end:
			found_flag = True
			break

		child = current.child_opt(forb)
		change = False

		for x in child:
			exi = False
			for y in expanded:
				if (x.value == y.value) and (x.prev_change == y.prev_change):
					exi = True
					break
			if exi == False:
				if get_heuristic(x.value, end) <= get_heuristic(current.value, end):
					change = True
					current = x
		if change == False:
			break

	if found_flag == True:
		first_line = []
		first_line.append(end)
		while current.parent != None:
			first_line.append(current.parent.value)
			current = current.parent
		first_line.reverse()
		print(",".join(first_line))
	else:
		print("No solution found")
	second_line = []
	for x in expanded:
		second_line.append(x.value)
	print(",".join(second_line))

def astar(start, end, forb):
	root = node(start, None, 0, 0)
	fringe = []
	expanded = []
	found_flag = False

	fringe.append(root)

	while found_flag == False and len(expanded) < 1000 and len(fringe) > 0:
		current = fringe.pop(0)
		expanded.append(current)

		if current.value == end:
			found_flag = True
			break

		child = current.child_opt(forb)
		for x in child:
			exi = False
			for z in expanded:
				if (z.value == x.value) and (z.prev_change == x.prev_change):
					exi = True
					break
			if exi == False:
				idx = 0
				for y in fringe:
					if get_heuristic(y.value, end_state) + y.depth >= get_heuristic(x.value, end_state) + x.depth:
						break
					idx += 1
				fringe.insert(idx, x)

	if found_flag == True:
		first_line = []
		first_line.append(end)
		while current.parent != None:
			first_line.append(current.parent.value)
			current = current.parent
		first_line.reverse()
		print(",".join(first_line))
	else:
		print("No solution found")
	second_line = []
	for x in expanded:
		second_line.append(x.value)
	print(",".join(second_line))

if __name__ == "__main__":

	#Reading inputs
	command = sys.argv[1]
	file = open(sys.argv[2], "r")
	file_line = file.read().split("\n")
	start_state = str(file_line[0])
	end_state = str(file_line[1])
	forbidden_state = []
	try:
		forbidden_state = file_line[2].split(",")
	except:
		pass

	if command == "B":
		bfs(start_state, end_state, forbidden_state)
	elif command == "D":
		dfs(start_state, end_state, forbidden_state)
	elif command == "I":
		ids(start_state, end_state, forbidden_state)
	elif command == "G":
		greedy(start_state, end_state, forbidden_state)
	elif command == "H":
		hill(start_state, end_state, forbidden_state)
	elif command == "A":
		astar(start_state, end_state, forbidden_state)
