import sys # Final

##################################################START OF CLASS##################################################
'''
Class Node
    This class helps to keep the tree structure when implementing the algorithm. 
    There are also some helper method for the algorithm.
'''
class Node:
    # Initializing
    def __init__(self, state, prevDigit, parent):
        self.state = state      #stores the number ex) 001, 003
        self.prevDigit = prevDigit      # Stores the previous digit that got changed. ex) if 001 -> 101 then prevDigit will be 100. 
        self.parent = parent        # stores the parent node when expanding.
        
        if None == parent: 
            self.height = 0     # If it doesn't have parents it's the root node
        else:
            self.height = self.parent.height + 1    # Else it will increment one to the height of the parents

    #----End of initialization----

    # This function will return the list of child based on the rules of spec sheet. 
    def getChildList(self):

        childList = []      # Creating an empty child list that will be returned

        # First condition. It will update the first digit, if it wasn't changed previously
        if self.prevDigit != 100:

            if self.state < 100 :   #We can only add 100. We can't subtract from 0
                childList.append(Node(self.state + 100, 100, self))

            else:
                # returns the first digit
                digit = (self.state // 100) % 10

                if digit >= 1 :
                    childList.append(Node(self.state - 100, 100, self))     # subtract 1 from the first digit
                if digit < 9: 
                    childList.append(Node(self.state + 100, 100, self))     # add 1 to the first digit
        
        # Second condition. It will update the second digit if it wasn't changed previously.
        if self.prevDigit != 10:
            if self.state < 10 :
                childList.append(Node(self.state + 10, 10, self))

            else:
                # returns the second digit 
                digit = (self.state // 10) % 10

                if digit >= 1 :
                    childList.append(Node(self.state - 10, 10, self))   # Subtract 1 from the first digit
                if digit < 9: 
                    childList.append(Node(self.state + 10, 10, self))   # Add 1 to the first digit
        
        # Third condition. It will update the third digit if it wasn't changed previously
        if self.prevDigit != 1:
            if self.state < 1 :
                childList.append(Node(self.state + 1, 1, self))
            
            else:
                # returs the third digit
                digit = (self.state) % 10

                if digit >= 1 :
                    childList.append(Node(self.state - 1, 1, self))     # Subtract 1 from the third digit
                if digit < 9: 
                    childList.append(Node(self.state + 1, 1, self))     # add 1 to the third digit
                    
        return childList

    #----child list returning done----

    # Returns true if the nodeList already contains it self. 
    def doesExist(self, nodeList):

        for node in nodeList:
            #If they have the same number alongside the same previous digit it means that they will have the same child.
            if (node.state == self.state) and (node.prevDigit == self.prevDigit):
                return True
                
        return False
    
    # Returns the absoulute difference for Manhattan heuristic
    def getDistance(self, goal):
        return abs((self.state % 10) - (goal % 10)) + abs((self.state // 10 % 10) - (goal // 10 % 10)) + abs((self.state // 100 % 10) - (goal // 100 % 10))

###################################################END OF CLASS###################################################

# Prints the final output when the goal node is found
def printFinal(goal, expanded):
    
    firstLine = ""

    # Iteratate from the goal node to the parent and contcatinate into string.
    while not goal.parent == None:
        firstLine = ",{:03}{}".format(goal.state, firstLine)
        goal = goal.parent
        
    firstLine = "{:03}{}".format(goal.state, firstLine)

    print(firstLine)

    # This will print the second line
    printExpanded(expanded)

    return

# Prints the second line of output
def printExpanded(expanded):
    secondLine = ""

    # Concatinate all the expanded string.
    while len(expanded) != 1:
        secondLine = "{}{:03},".format(secondLine, expanded.pop(0).state)

    secondLine = "{}{:03}".format(secondLine, expanded.pop(0).state)

    print(secondLine)

    return

#------------End of Printing Functions------------#

def bfs(start, goal, forbidden):
    
    expanded = []       # Stores the expanded node
    fringe = []        # Stroes the node in the fringe array

    node = Node(start, 0, None)     # creats a node with the starting state. (which will be the root of the tree)
    fringe.append(node)     # Add it to the fringe
    found = False

    while len(expanded) < 1000 and len(fringe) != 0: 

        # Remove the node form the fringe and add it to the expanded node
        temp = fringe[0]
        expanded.append(temp)
        fringe.pop(0)

        if temp.state == goal: # The goal state has been found
            found = True
            printFinal(temp, expanded)
            break

        childList = temp.getChildList() # Getting the list of the child node. (implemented in the class "Node")

        # If the childist includes child node that are in the forbidden list or expanded list or in the fringe list we don't add it to the fringe.
        for child in childList:     
            if (child.state not in forbidden) and (not child.doesExist(expanded)) and (not child.doesExist(fringe)):
                fringe.append(child)
                
    # If not found then print out the expanded list.  
    if found == False:
        print("No solution found")
        printExpanded(expanded)
        
        
    return

#------------End of BFS------------#

def dfs(start, goal, forbidden):

    expanded = []       # Stores the expanded node
    fringe = []     # Stores the node in the fringe array

    node = Node(start, 0, None)     # Creates the node with the starting state
    fringe.append(node)     # Append it the the fringe
    found = False
    
    while len(expanded) < 1000 and len(fringe) != 0: 

        temp = fringe[0]        # Remove the first element from the fringe and add it the the expanded list

        if(temp.doesExist(expanded)): # If the temp already exist inthe expanded node just skip it.
            fringe.pop(0)
            continue

        expanded.append(temp)
        fringe.pop(0)

        if temp.state == goal:      # The goal state has been reached
            found = True
            printFinal(temp, expanded)      # Print the final result
            break

        childList = temp.getChildList()
        k = 0   
        length = len(childList)
        
        # Doing the same as BFS however we are adding the child node to the front of the fringe instead of appending it at the end.
        for child in childList:
            if (child.state not in forbidden) and (not child.doesExist(expanded)):
                fringe.insert(k, child)
                k = k + 1 
        
    if found == False:
        print("No solution found")
        printExpanded(expanded)
        
    return

#------------End of DFS------------#

def ids(start, goal, forbidden):

    expanded = []   # Stores the expanded node
    depth = 0       # Stores the allowed depth
    found = False

    while len(expanded) < 1000:         # Total length of the expanded node has to be less than the 1,000 

        levelExpanded = []      # Expanded Node per level. It will be appended the expande list later at the end of the while loop
        fringe = []     # New fringe per level

        node = Node(start, 0, None)     # Initializing node with the start state
        fringe.append(node)         # First add the item to the fringe

        # This innder while loop will add simillarly to the DFS search algorihtm
        while (len(expanded) + len(levelExpanded)) < 1000 and len(fringe) != 0:        

            temp = fringe[0]
            fringe.pop(0)
            
            if(not temp.doesExist(levelExpanded)):      # Check if the temp already exist inthe level expanded list. Only add if it doesn't exist. 

                levelExpanded.append(temp)

                if temp.state == goal:

                    for node in levelExpanded:  # If the goal state has been reached apppend all the node that is in the levelexpanded list to the expanded list.
                        expanded.append(node)
                    
                    found = True
                    printFinal(temp, expanded)
                    break

                if temp.height < depth: # Only consider node that are within the depth range

                    childList = temp.getChildList()
                    k = 0   
                
                    for child in childList:     # Add item to the fringe if it does not exist in the level expanded
                        if (child.state not in forbidden) and (not child.doesExist(levelExpanded)):
                            fringe.insert(k, child)
                            k = k + 1 
        
        for node in levelExpanded:      # Add all the node in level expanded not to the expanded list for printing the result at the end of the algorithm.
            expanded.append(node)
        depth = depth + 1

        if found == True:
            break

    if found == False:
        print("No solution found")
        printExpanded(expanded)                  
                          
    return

#------------End of IDS------------#

def greedy(start, goal, forbidden):

    expanded = []       # Stores the expanded node
    fringe = []     # Stored the fringe node

    node = Node(start, 0, None)     # Creates and initialize the starting node
    fringe.append(node)
    found = False

    while len(expanded) < 1000 and len(fringe) != 0: 

        temp = fringe[0]
        fringe.pop(0)

        if(temp.doesExist(expanded)):       # If the item already exist int the expanded node skip and and continue with the next iteration
            continue

        expanded.append(temp)       

        if temp.state == goal:
            found = True
            printFinal(temp, expanded)
            break

        childList = temp.getChildList()
        k = 0   

        for child in childList:     # Find the correct index from using greedyInded function insert it in to the fringe
            if (child.state not in forbidden) and (not child.doesExist(expanded)):
                k = greedyIndex(fringe, child, goal)
                fringe.insert(k, child)
                
        
    if found == False:
        print("No solution found")
        printExpanded(expanded)
        
    return

# Calculates the greedy index
def greedyIndex(fringe, child, goal):
    i = 0
    for item in fringe:     #Here distance is implemented in the class "Node"
        if item.getDistance(goal) >= child.getDistance(goal):
            return i
        i += 1
    return i

#------------End of Greedy-----------#

def hill(start, goal, forbidden):
    expanded = []       # Stroes the expanded node
    node = Node(start, 0, None)     # Initialize the node with the start state

    while len(expanded) < 1000: 

        expanded.append(node)              

        if(node.state == goal):     # If the goal node has been reached then stop the process 
            printFinal(node, expanded)
            break
        
        childList = node.getChildList()
        
        swapped = False     # Initialized the swap to be false

        for child in childList:     # Will add the last child that satifies the condition to and expand it later
            if (child.state not in forbidden) and (not child.doesExist(expanded)):
                if(child.getDistance(goal) <= node.getDistance(goal)):
                    swapped = True
                    node = child

        if swapped == False:
            print("No solution found")
            printExpanded(expanded)
            break

        
    return

#------------End of Hill Climbing------------#

def aStar(start, goal, forbidden):
    expanded = []       # List of expanded node
    fringe = []     # list of fringe nodes

    node = Node(start, 0, None)     #Initialize the node
    fringe.append(node)     # Append it into the fringe array first
    found = False

    while len(expanded) < 1000 and len(fringe) != 0: 

        temp = fringe[0]    
        fringe.pop(0)       # Pop the item from the fringe

        if(temp.doesExist(expanded)):       #Skip if it already exist in the expanded list
            continue

        expanded.append(temp)       # Adding temp node to the expanded array 


        if temp.state == goal:
            found = True
            printFinal(temp, expanded)
            break

        childList = temp.getChildList()
        k = 0   
            
        for child in childList:     # find the a correct index using aStarIndex function and add it to the corresponding index
            if (child.state not in forbidden) and (not child.doesExist(expanded)):
                k = aStarIndex(fringe, child, goal)
                fringe.insert(k, child)
                 
        
    if found == False:
        print("No solution found")
        printExpanded(expanded)
        
    return

# Returns the index of the node to be added in the fringe list.
def aStarIndex(fringe, child, goal):
    i = 0
    for item in fringe:
        if item.getDistance(goal) + item.height >= child.getDistance(goal) + child.height:
            return i
        i += 1
    return i

#------------End of A*------------#

"""
MAIN FUNTION
"""
if __name__ == "__main__":
    
    try:
        algorithm = str(sys.argv[1])        # User specified algorithm type. Ex) G for Greedy, H for hill climbing and etc
        filePath = str(sys.argv[2])

        #Start and goal state stored as integer  
        start = 0
        goal = 0

        #forbidden as empty integer array
        forbidden = []

        textFile = open(filePath, 'r')
        lines = textFile.readlines()

        #Saving the start and goal variable
        start = int(lines[0].strip('\n'))
        goal = int(lines[1].strip('\n'))

        #If there is forbidden provided save it into forbidden array as integers
        if 3 == len(lines):
            forbidden = list(map(int, lines[2].split(",")))

        # Assigning start, goal forbidden to each algorithms.     
        if algorithm == "B" : bfs(start, goal, forbidden)
        elif algorithm == "D" : dfs(start, goal, forbidden)
        elif algorithm == "I" : ids(start, goal, forbidden)
        elif algorithm == "G" : greedy(start, goal, forbidden)
        elif algorithm == "H" : hill(start, goal, forbidden)
        elif algorithm == "A" : aStar(start, goal, forbidden) 
        
        textFile.close()

    except Exception as e:
        print("No Solution Found")
        print(e)
    