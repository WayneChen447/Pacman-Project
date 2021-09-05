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

--------------------------------------------------------------------------------

 if (problem.isGoalState(state)): return 0
    distances = []
    num = len(corners)
    s_to_c1 = sqrt( (state[0][0] - corners[0][0])**2 + (state[0][1] - corners[0][1])**2)
    s_to_c2 = sqrt( (state[0][0] - corners[1][0])**2 + (state[0][1] - corners[1][1])**2)
    s_to_c3 = sqrt( (state[0][0] - corners[2][0])**2 + (state[0][1] - corners[2][1])**2)
    s_to_c4 = sqrt( (state[0][0] - corners[3][0])**2 + (state[0][1] - corners[3][1])**2)
    s_to_c = [s_to_c1, s_to_c2, s_to_c3, s_to_c4]
    for i in range(num):
        d1 = s_to_c[i]
        for j in range(num):
            if (j == i): continue
            d2 = sqrt( (corners[i][0] - corners[j][0])**2 + (corners[i][1] - corners[j][1])**2)
            for k in range(num):
                if (k == i or k == j): continue
                d3 = sqrt( (corners[j][0] - corners[k][0])**2 + (corners[j][1] - corners[k][1])**2)
                for z in range(num):
                    if (z == i or z == j or z == k): continue
                    d4 = sqrt( (corners[k][0] - corners[z][0])**2 + (corners[k][1] - corners[z][1])**2) 
                    distances.append(d1 + d2 + d3 + d4)
    return min(distances)