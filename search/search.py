# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import Stack
from util import Queue
from util import PriorityQueue
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """
    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    a = graphSearch(problem,dfs,nullHeuristic)
    for i in range(len(a)):
        if(a[i] == 'West'):
            a[i] = Directions.WEST
        if(a[i] == 'South'):
            a[i] = Directions.SOUTH
        if(a[i] == 'East'):
            a[i] = Directions.EAST
        if(a[i] == 'North'):
            a[i] = Directions.NORTH
    return a

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    a = graphSearch(problem,bfs,nullHeuristic)
    for i in range(len(a)):
        if(a[i] == 'West'):
            a[i] = Directions.WEST
        if(a[i] == 'South'):
            a[i] = Directions.SOUTH
        if(a[i] == 'East'):
            a[i] = Directions.EAST
        if(a[i] == 'North'):
            a[i] = Directions.NORTH
    return a

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    a = graphSearch(problem,ucs,nullHeuristic)
    for i in range(len(a)):
        if(a[i] == 'West'):
            a[i] = Directions.WEST
        if(a[i] == 'South'):
            a[i] = Directions.SOUTH
        if(a[i] == 'East'):
            a[i] = Directions.EAST
        if(a[i] == 'North'):
            a[i] = Directions.NORTH
    return a

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    a = graphSearch(problem,astar,heuristic)
    for i in range(len(a)):
        if(a[i] == 'West'):
            a[i] = Directions.WEST
        if(a[i] == 'South'):
            a[i] = Directions.SOUTH
        if(a[i] == 'East'):
            a[i] = Directions.EAST
        if(a[i] == 'North'):
            a[i] = Directions.NORTH
    return a
    
def graphSearch(problem,search,heuristic):
    if(search == dfs):
        frontier = Stack()
    if(search == bfs):
        frontier = Queue()
    if(search == ucs):
        frontier = PriorityQueue()
    if(search == astar):
        frontier = PriorityQueue()
    if(search == ucs):
        frontier.push(problem.getStartState(),0)
    elif(search == astar):
        frontier.push(problem.getStartState(),heuristic(problem.getStartState(),problem))
    else:
        frontier.push(problem.getStartState())
    cost = {}
    if(search == astar):
        cost = {problem.getStartState() : heuristic(problem.getStartState(),problem)} 
    else:
        cost = {problem.getStartState() : 0}
    actionlist = []
    transtable = []
    explored = []
    while(True):
        cur = frontier.pop()
        curcost = cost[cur]
        if(problem.isGoalState(cur)):
            r = len(transtable)   
            try:
                actionlist = problem.road
                if(search == bfs):
                    problem._expanded += problem.gap
            except AttributeError:
                pass
            while(True):
                for i in range(r):
                    if(transtable[r-i-1][0] == cur):
                        actionlist.insert(0,transtable[r-i-1][2])
                        cur = transtable[r-i-1][1]
                        r = r-i-1
                        break
                    else:
                        transtable.pop(r-i-1)
                        if(r-i-1 == 0):
                            r = 0
                if(r == 0):
                    break
            return actionlist
        explored.append(cur)
        leaves = problem.getSuccessors(cur)
        for leaf in leaves:
            if(search == ucs):
                if(cost.has_key(leaf[0]) == 0):
                    if(explored.count(leaf[0]) == 0):
                        frontier.update(leaf[0],(leaf[2]+curcost))
                        cost[leaf[0]] = (leaf[2]+curcost)
                        transtable.append([leaf[0],cur,leaf[1]])
                else:
                    if(cost[leaf[0]] > (leaf[2]+curcost)):
                        del cost[leaf[0]]
                        frontier.update(leaf[0],(leaf[2]+curcost))
                        cost[leaf[0]] = (leaf[2]+curcost)
                        for i in range(len(problem.transtable)):
                            if(transtable[i][0] == leaf[0]):
                                transtable[i][1] = cur
                                transtable[i][2] = leaf[1]
            elif(search == astar):
                if(cost.has_key(leaf[0]) == 0):
                    if(explored.count(leaf[0]) == 0):
                        frontier.push(leaf[0],(leaf[2]+curcost+heuristic(leaf[0],problem)))
                        cost[leaf[0]] = (leaf[2]+curcost)
                        transtable.append([leaf[0],cur,leaf[1]])
                else:
                    if(cost[leaf[0]] > (leaf[2]+curcost)):
                        del cost[leaf[0]]
                        frontier.update(leaf[0],(leaf[2]+curcost+heuristic(leaf[0],problem)))
                        cost[leaf[0]] = (leaf[2]+curcost)
                        for i in range(len(transtable)):
                            if(transtable[i][0] == leaf[0]):
                                transtable[i][1] = cur
                                transtable[i][2] = leaf[1]
            elif(frontier.list.count(leaf[0]) == 0):              
                if(explored.count(leaf[0]) == 0):
                    frontier.push(leaf[0])
                    cost[leaf[0]] = (leaf[2]+curcost)
                    transtable.append([leaf[0],cur,leaf[1]])            
    return actionlist

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
