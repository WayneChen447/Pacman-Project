# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import sys
from Queue import PriorityQueue

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    visited = {}
    search_list = []
    'The key is a position and the values are its predecessor and the direction'
    predecessors = {}
    'The second element is the direction which its predecessor goes to this position.'
    search_list.insert(0, (problem.getStartState(), None, None))
    FindGoal = False
    goal = (0, 0)
    
    while (len(search_list) > 0):
        pos = search_list.pop(0)
        if visited.get(pos[0]) == True:
            continue
        predecessors[pos[0]] = (pos[1], pos[2])
        if problem.isGoalState(pos[0]):
            goal = pos[0]
            FindGoal = True
            break
        successors = problem.getSuccessors(pos[0])
        for successor in successors:
            search_list.insert(0, (successor[0], pos[0], successor[1]))
        visited[pos[0]] = True
        
    actions = []
    if (FindGoal):
        while True:
            predecessor = predecessors.get(goal)
            if predecessor[1] == None:
                break
            else:
                actions.insert(0, predecessor[1])
                goal = predecessor[0]
    else:
        sys.stderr.write("This maze doesn't have a path to the goal\n")
        exit(1)
        
    return actions

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    
    visited = {}
    search_list = []
    'The key is a position and the values are its predecessor and the direction'
    predecessors = {}
    'The second element is the direction which its predecessor goes to this position.'
    search_list.insert(0, (problem.getStartState(), None, None))
    FindGoal = False
    goal = (0, 0)

    
    while (len(search_list) > 0):
        pos = search_list.pop()
        if visited.get(pos[0]) == True:
            continue
        predecessors[pos[0]] = (pos[1], pos[2])
        if problem.isGoalState(pos[0]):
            goal = pos[0]
            FindGoal = True
            break
        successors = problem.getSuccessors(pos[0])
        for successor in successors:
            search_list.insert(0, (successor[0], pos[0], successor[1]))
        visited[pos[0]] = True
        
    actions = []
    if (FindGoal):
        while True:
            predecessor = predecessors.get(goal)
            if predecessor[1] == None:
                break
            else:
                actions.insert(0, predecessor[1])
                goal = predecessor[0]
    else:
        sys.stderr.write("This maze doesn't have a path to the goal\n")
        exit(1)
        
    return actions

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    visited = {}
    search_list = PriorityQueue()
    'The key is a position and the values are its predecessor and the direction'
    predecessors = {}
    'The second element is the direction which its predecessor goes to this position.'
    search_list.put((0, problem.getStartState(), None, None))
    FindGoal = False
    goal = (0, 0)
    
    while (not search_list.empty()):
        pos = search_list.get()
        if visited.get(pos[1]) == True:
            continue
        predecessors[pos[1]] = (pos[2], pos[3])
        if problem.isGoalState(pos[1]):
            goal = pos[1]
            FindGoal = True
            break
        successors = problem.getSuccessors(pos[1])
        for successor in successors:
            search_list.put((pos[0] + successor[2], successor[0], pos[1], successor[1]))
        visited[pos[1]] = True
        
    actions = []
    if (FindGoal):
        while True:
            predecessor = predecessors.get(goal)
            if predecessor[1] == None:
                break
            else:
                actions.insert(0, predecessor[1])
                goal = predecessor[0]
    else:
        sys.stderr.write("This maze doesn't have a path to the goal\n")
        exit(1)
        
    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    visited = {}
    search_list = PriorityQueue()
    'The key is a position and the values are its predecessor and the direction'
    predecessors = {}
    'The second element is the direction which its predecessor goes to this position.'
    search_list.put((0 + heuristic(problem.getStartState(), problem), 0, problem.getStartState(), None, None))
    FindGoal = False
    goal = (0, 0)
    
    while (not search_list.empty()):
        pos = search_list.get()
        if visited.get(pos[2]) == True:
            continue
        predecessors[pos[2]] = (pos[3], pos[4])
        if problem.isGoalState(pos[2]):
            goal = pos[2]
            FindGoal = True
            break
        successors = problem.getSuccessors(pos[2])
        for successor in successors:
            search_list.put((pos[1] + successor[2] + heuristic(successor[0], problem), pos[1] + successor[2], successor[0], pos[2], successor[1]))
        visited[pos[2]] = True
        
    actions = []
    
    if (FindGoal):
        while True:
            predecessor = predecessors.get(goal)
            if predecessor[1] == None:
                break
            else:
                actions.insert(0, predecessor[1])
                goal = predecessor[0]
    else:
        sys.stderr.write("This maze doesn't have a path to the goal\n")
        exit(1)
        
    return actions
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
