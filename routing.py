import picar_4wd as fc
import numpy as np
import time
from heapq import *
from advancedMapping import buildMap

# nodes as 1x1cm grid cells in map
class Node:
    def __init__(self, parent, coordinates, cost, action):
        self.parent = parent
        self.coordinates = coordinates
        self.cost = cost
        self.action = action

    # heap operations
    def __gt__(self, other):
        return self.cost > other.cost

    def __lt__(self, other):
        return self.cost < other.cost

# traverses through parent pointers to get A* path
def getPath(node):
    path = []
    currNode = node
    while currNode.parent:
        path.append(currNode.coordinates)
        currNode = currNode.parent
    return path[::-1]

def AStar(Map, start, end):
    # forward, right, backward, left
    ACTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    frontier = [start] # nodes to visit, sorted by least cost to highest cost
    explored = [] # nodes visited

    # list of obstacles for clearance
    obstacles = []
    for x in range(0,100):
        for y in range(0,50):
            if Map[x,y] == 1:
                obstacles.append((x,y))

    # add clearance to obstacles by adding them to explored list
    r = 1
    for obstacle in obstacles:
        top =    obstacle[1] + r
        bottom = obstacle[1] - r
        left =   obstacle[0] - r
        right =  obstacle[0] + r

        for x in range(left, right+1):
            for y in range(bottom, top + 1):
                explored.append((x,y))

    # A*
    while True:
        currNode = heappop(frontier) # Pops least cost node

        coords = currNode.coordinates # current coordinate
        totalCost = currNode.cost # current cost

        # get path when A* reaches end
        if coords == end.coordinates:
            path = getPath(currNode)
            return path

        # get children in each direction
        children = [(coords[0] + a[0], coords[1] + a[1]) for a in ACTIONS]

        explored.append(coords) # mark as explored

        for child in children:
            if child[0] in range(0,100) and child[1] in range(0,50): # Checks if child is within graph

                if Map[child] != 1: # Checks this cell is an obstacle
                    action = (np.abs(coords[0] - child[0]), np.abs(coords[1] - child[1])) # determine what action has lead here

                    # forward has least cost, backward most cost, right and left in between
                    cost = 0
                    if action == (0,1): # forward:
                        cost = 1
                    elif action == (1,0) or action == (-1,0): # right or left
                        cost = 2
                    else: # backward
                        cost = 3
                    
                    g = totalCost + cost # total cost up to this node
                    h = ((child[0] - end.coordinates[0]) ** 2) + ((child[1] - end.coordinates[1]) ** 2) # euclidian distance
                    f = g + h # cost including heuristic

                    # Checks if not explored and not in the frontier
                    if child not in explored and child not in [x.coordinates for x in frontier]:
                        # create node to put on heap: parent, coordinates, cost
                        newNode = Node(currNode, child, g, action)
                        heappush(frontier, newNode)

                    # Checks if in the frontier and not explored
                    elif child in [x.coordinates for x in frontier]:
                        # if there exists a lower cost path to this same node, replace the higher cost node
                        if [x.cost for x in frontier if x.coordinates == child][0] > f:
                            newNode = Node(currNode, child, g, action)
                            # remove node with old cost
                            frontier.remove(([x.cost for x in frontier if x.coordinates == child][0], child))
                            # add new lower cost node to heap
                            heappush(frontier, newNode)

def routing(origin, destination):
    # Create nodes for start, end
    start = Node(None, origin, 0, None)
    end = Node(None, destination, 0, None)

    # scan, create map of surroundings
    Map = buildMap(False)

    # calculate A* path
    path = AStar(Map, start, end)

    # mark path with 7
    for coord in path:
        Map[coord] = 7

    # follow path of 7's
    if 7 == Map[49,1]:
        fc.forward(20)
        time.sleep(.1) # 3cm
        fc.stop()
        destination = (destination[0], destination[1] - 3)
    elif 7 == Map[48,0]:
        fc.turn_left(100)
        time.sleep(1)
        fc.stop()
        destination = (destination[1] + 49, -(destination[0] - 49)) #clockwise rotation
    elif 7 == Map[50, 0]:
        fc.turn_right(100)
        time.sleep(0.5)
        fc.stop()
        destination = (-destination[1] + 49, destination[0] - 49) #counter clockwise rotation

    # Reached destination
    if destination[0] == origin[0] and destination[1] == origin[1]:
        return None

    return destination

def main():
    # first setup
    start1 = (49,0)
    destination1 = (7,39)
    while destination1 != None:
        destination1 = routing(start1, destination1)

    # stop to indicate next path starting
    fc.stop()
    time.sleep(5)

    # second setup
    start2 = (49,0)
    destination2 = (85,48)
    while destination2 != None:
        destination2 = routing(start2, destination2)
        
if __name__ == "__main__":
    main()
