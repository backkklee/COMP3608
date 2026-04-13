import sys
from heapq import heappush, heappop

global treasures
global n, m, grid, start, heuristics, teleports
global directions
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

'''
teleports is a dictionary that maps the teleport's entrance to its exit
key: teleport number, value: (x, y) coordinates of the teleport's exit
'''
def read_input(filename):    
    with open(filename, 'r') as f:
        line = f.readline().strip()
        global n, m
        m, n = map(int, line.split('x'))
        line = f.readline().strip()
        global start
        start = tuple(map(int, line.split('-')))
        lines = f.readlines()
        global grid
        grid = []
        for line in lines:
            grid.append(list(line.strip()))
    global treasures
    treasures = []
    global teleports
    teleports = {}
    #Find treasures and teleports
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'X':
                treasures.append((i, j))
            if (grid[i][j].isnumeric()):
                teleports[ord(grid[i][j]) - ord('0')] = (j, i)

def heuristic(x, y):
    # Manhattan distance to the closest treasure
    min_dist = n + m
    for treasure in treasures:
        dist = abs(x - treasure[0]) + abs(y - treasure[1])
        min_dist = min(min_dist, dist)
    return min_dist

def calculate_heuristics():
    global heuristics
    heuristics = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            heuristics[i][j] = heuristic(i, j)
    # Heuristics for teleport's entrance is the same as its exit
    for i in range(1, len(teleports), 2):
        heuristics[teleports[i][1]][teleports[i][0]] = heuristics[teleports[i + 1][1]][teleports[i + 1][0]]

def output(strat, expanded, path, cost):
    print(f"{strat} Search Initiated")
    print(f"Expanded: {''.join(f'({x}, {y})' for x, y in expanded)}")
    if (not path):
        print("NO PATH FOUND!")
        return
    print(f"Path Found: {path}")
    print(f"Taking this path will cost: {cost} Willpower")

def BFS():
    fringe =[start]
    expanded = []
    visited = set([start])
    goal_founded = False
    parent = {}     #use dictionary to keep track each node's parent - trace back path from goal to start

    while fringe:
        cur = fringe.pop(0)
        expanded.append(cur)

        # Stop when expanded a goal tile "X"
        if (grid[cur[1]][cur[0]] == "X"):
            goal_founded = True
            break
        
        # Handle special tiles: Portal
        if (grid[cur[1]][cur[0]].isnumeric() and ord(grid[cur[1]][cur[0]]) % 2 == 1):
            teleport_exit = teleports[ord(grid[cur[1]][cur[0]]) - ord('0') + 1]
            parent[teleport_exit] = (cur[0], cur[1])
            visited.add(teleport_exit)
            fringe.append(teleport_exit)
            continue

        for d in directions:
            # compute all possible next position in next move
            new_x = cur[0] + d[0]
            new_y = cur[1] + d[1]

            # Ignore positions that are outside the given range mxn
            if (new_x >= m or new_x < 0 or new_y >= n or new_y < 0):
                continue 
            
            # Handle special tiles: Wall
            if (grid[new_y][new_x] == "W"):
                continue
                
            new_node = (new_x, new_y)
            if new_node not in visited:
                visited.add(new_node)
                fringe.append(new_node)
                parent[new_node] = cur  # Set parent-child relationship to cur-new_node
    
    # If no goal tiles founded, return message
    if not goal_founded:
        output("BFS", expanded, [], 0)

    # Trace back from goal to start tile then print out the path
    path = []
    cost = 0
    cur = expanded[-1]
    while cur in parent.keys():
        if grid[cur[1]][cur[0]] == 'M':
            cost += 2
        elif grid[cur[1]][cur[0]] == 'B':
            cost += 3
        elif grid[cur[1]][cur[0]].isnumeric() and ord(grid[cur[1]][cur[0]]) % 2 == 1:
            cost += 0
        else:
            cost += 1
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    path.reverse()
    output("BFS", expanded, path, cost)

def UCS():
    fringe = [(0, start)]
    expanded = []
    visited = set()
    goal_founded = False
    parent = {}
    cost_so_far = {start: 0}    # Tracks the best known cost to each visited node

    while fringe:
        pop = heappop(fringe)
        current_cost = pop[0]
        current_node = pop[1]
        x, y = current_node

        # Skip already expanded nodes
        if current_node in expanded:
            continue

        expanded.append(current_node)

        # Stop when treasure tile is expanded
        if grid[y][x] == "X":
            goal_founded = True
            break

        # Handle teleport tiles - additional 1 cost to move on portal tile
        elif grid[y][x].isnumeric() and ord(grid[y][x]) % 2 == 1:
            teleport_exit = teleports[ord(grid[y][x]) - ord('0') + 1]
            if teleport_exit not in expanded:
                parent[teleport_exit] = (x, y)
                cost_so_far[teleport_exit] = current_cost
                heappush(fringe, (current_cost, teleport_exit))
            continue

        for d in directions:
            new_x = x + d[0]
            new_y = y + d[1]

            if (new_x >= m or new_x < 0 or new_y >= n or new_y < 0):
                continue
            if grid[new_y][new_x] == "W":
                continue

            new_node = (new_x, new_y)
            # # Compute the next movement cost based on tile types
            if grid[new_y][new_x] == 'M':
                total_cost = current_cost + 2
            elif grid[new_y][new_x] == 'B':
                total_cost = current_cost + 3
            else:
                total_cost = current_cost + 1

            if new_node not in expanded and total_cost < cost_so_far.get(new_node, float('inf')):
                cost_so_far[new_node] = total_cost
                heappush(fringe, (total_cost, new_node))
                parent[new_node] = current_node

    if not goal_founded:
        output("UCS", expanded, [], 0)
        return

    # Trace back from goal to start
    path = []
    cost = 0
    cur = expanded[-1]
    while cur in parent:
        if grid[cur[1]][cur[0]] == 'M':
            cost += 2
        elif grid[cur[1]][cur[0]] == 'B':
            cost += 3
        elif grid[cur[1]][cur[0]].isnumeric() and ord(grid[cur[1]][cur[0]]) % 2 == 1:
            cost += 0  # entrance costs 1 willpower to move onto
        else:
            cost += 1
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    path.reverse()
    output("UCS", expanded, path, cost)

def IDS(limit):
    expanded = []
    goal_founded = False

    for l in range(limit+1):
        fringe = [(start, 0)]
        visited = set()
        parent = {}

        if goal_founded:
            break

        while fringe:
            current_node, depth = fringe.pop(-1)   #we expand from the bottom to search for the depth first
            x,y = current_node
            
            if depth > l:
                continue

            if current_node in visited:
                continue

            visited.add(current_node)
            expanded.append(current_node)

            # Stop when expanded a goal tile "X"
            if (grid[y][x] == "X"):
                goal_founded = True
                break
            
            # Handle special tiles: Portal
            if (grid[y][x].isnumeric() and ord(grid[y][x]) % 2 == 1):
                teleport_exit = teleports[ord(grid[y][x]) - ord('0') + 1]
                fringe.append((teleport_exit,depth+1))
                parent[teleport_exit] = (x, y)
                continue
            
            for r in reversed(directions):
                # compute all possible next position in next move
                new_x = x + r[0]
                new_y = y + r[1]
                
                # Ignore positions that are outside the given range mxn
                if (new_x >= m or new_x < 0 or new_y >= n or new_y < 0):
                    continue 
                
                # Handle special tiles: Wall
                if (grid[new_y][new_x] == "W"):
                    continue
                    
                new_node = (new_x, new_y)
                if new_node not in visited:
                    fringe.append((new_node,depth+1))
                    parent[new_node] = current_node 

    if not goal_founded:
        output("IDS", expanded, [], 0)
        return

    # Trace back from goal to start tile then print out the path
    path = []
    cost = 0
    cur = expanded[-1]
    while cur in parent.keys():
        if grid[cur[1]][cur[0]] == 'M':
            cost += 2
        elif grid[cur[1]][cur[0]] == 'B':
            cost += 3
        elif grid[cur[1]][cur[0]].isnumeric() and ord(grid[cur[1]][cur[0]]) % 2 == 1:
            cost += 0
        else:
            cost += 1
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    path.reverse()

    output("IDS", expanded, path, cost)

def Greedy():
    fringe = []
    added = set()
    expanded = []
    parents = {}
    heappush(fringe, (0, start))
    added.add(start)
    finished = 0
    while fringe:
        x, y = heappop(fringe)[1]
        expanded.append((x, y))
        if grid[y][x] == 'X':
            finished = 1
            break
        elif grid[y][x].isnumeric() and ord(grid[y][x]) % 2 == 1:
            teleport_exit = teleports[ord(grid[y][x]) - ord('0') + 1]
            parents[teleport_exit] = (x, y)
            added.add(teleport_exit)
            heappush(fringe, (0, teleport_exit))
            continue
        for dir in directions:
            new_x = x + dir[0]
            new_y = y + dir[1]
            if (new_x < 0 or new_x >= m or new_y < 0 or new_y >= n):
                continue
            if (new_x, new_y) in added:
                continue
            # If the cell is a wall, skip it
            if grid[new_y][new_x] == 'W':
                continue
            parents[(new_x, new_y)] = (x, y)
            added.add((new_x, new_y))
            heappush(fringe, (heuristics[new_y][new_x], (new_x, new_y)))
    if not finished:
        output("Greedy", expanded, [], 0)
        return
    # Reconstruct the path
    path = []
    current = expanded[-1]
    cost = 0
    while current in parents:
        if grid[current[1]][current[0]] == 'M':
            cost += 2
        elif grid[current[1]][current[0]] == 'B':
            cost += 3
        elif grid[current[1]][current[0]].isnumeric() and ord(grid[current[1]][current[0]]) % 2 == 1:
            cost += 0
        else:
            cost += 1
        path.append(current)
        current = parents[current]
    path.append(start)
    path.reverse()
    output("Greedy", expanded, path, cost)



def A_star():
    fringe = []
    added = set()
    expanded = []
    parents = {}
    path_cost = {start: 0}
    heappush(fringe, (0, start))
    added.add(start)
    finished = 0
    while fringe:
        x, y = heappop(fringe)[1]
        expanded.append((x, y))
        if grid[y][x] == 'X':
            finished = 1
            break
        elif grid[y][x].isnumeric() and ord(grid[y][x]) % 2 == 1:
            teleport_exit = teleports[ord(grid[y][x]) - ord('0') + 1]
            parents[teleport_exit] = (x, y)
            path_cost[teleport_exit] = path_cost[(x, y)]
            added.add(teleport_exit)
            heappush(fringe, (0, teleport_exit))
            continue
        for dir in directions:
            new_x = x + dir[0]
            new_y = y + dir[1]
            if (new_x < 0 or new_x >= m or new_y < 0 or new_y >= n):
                continue
            if (new_x, new_y) in added:
                continue
            # If the cell is a wall, skip it
            if grid[new_y][new_x] == 'W':
                continue
            value = 1
            if grid[new_y][new_x] == 'M':
                value += 1
            elif grid[new_y][new_x] == 'B':
                value += 2
            parents[(new_x, new_y)] = (x, y)
            path_cost[(new_x, new_y)] = path_cost[(x, y)] + value
            added.add((new_x, new_y))
            heappush(fringe, (heuristics[new_y][new_x] + path_cost[(new_x, new_y)], (new_x, new_y)))
    
    if not finished:
        output("A*", expanded, [], 0)
        return
    # Reconstruct the path
    path = []
    current = expanded[-1]
    cost = 0
    while current in parents:
        if grid[current[1]][current[0]] == 'M':
            cost += 2
        elif grid[current[1]][current[0]] == 'B':
            cost += 3
        elif grid[current[1]][current[0]].isnumeric() and ord(grid[current[1]][current[0]]) % 2 == 1:
            cost += 0
        else:
            cost += 1
        path.append(current)
        current = parents[current]
    path.append(start)
    path.reverse()
    output("A*", expanded, path, cost)

def Beam(width):
    fringe = []
    added = set()
    expanded = []
    parents = {}
    heappush(fringe, (heuristics[start[1]][start[0]], start))
    added.add(start)
    finished = 0
    prev_best = n + m
    while not finished:
        candidates = []
        best = n + m
        for i in range(width): 
            if fringe:
                candidates.append(heappop(fringe))
                best = min(best, candidates[-1][0])
        if (best >= prev_best):
            break
        prev_best = best
        fringe = []
        for candidate in candidates:
            x, y = candidate[1]
            expanded.append((x, y))
            if grid[y][x] == 'X':
                finished = 1
                break

            if grid[y][x].isnumeric() and ord(grid[y][x]) % 2 == 1:
                '''
                teleport_exit = teleports[ord(grid[y][x]) - ord('0') + 1]
                if teleport_exit not in added:
                    parents[teleport_exit] = (x, y)
                    added.add(teleport_exit)
                    heappush(fringe, (heuristics[teleport_exit[1]][teleport_exit[0]], teleport_exit))
                '''
                continue

            for dir in directions:
                new_x = x + dir[0]
                new_y = y + dir[1]
                if (new_x < 0 or new_x >= m or new_y < 0 or new_y >= n):
                    continue
                if (new_x, new_y) in added:
                    continue
                # If the cell is a wall, skip it
                if grid[new_y][new_x] == 'W':
                    continue
                parents[(new_x, new_y)] = (x, y)
                added.add((new_x, new_y))
                heappush(fringe, (heuristics[new_y][new_x], (new_x, new_y)))
        if not fringe:
            break
    
    if not finished:
        output("Beam", expanded, [], 0)
        return
    # Reconstruct the path
    path = []
    current = expanded[-1]
    cost = 0
    while current in parents:
        if grid[current[1]][current[0]] == 'M':
            cost += 2
        elif grid[current[1]][current[0]] == 'B':
            cost += 3
        elif grid[current[1]][current[0]].isnumeric() and ord(grid[current[1]][current[0]]) % 2 == 1:
            cost += 0
        else:
            cost += 1
        path.append(current)
        current = parents[current]
    path.append(start)
    path.reverse()
    output("Beam", expanded, path, cost)


def main(strategy, filename, param):
    read_input(filename)
    #print(grid)
    calculate_heuristics()
    #print(heuristics)
    match strategy:
        case "B":
            BFS()
        case "U":
            UCS()
        case "I":
            IDS(param)
        case "G":
            Greedy()
        case "A":
            A_star()
        case "M":
            Beam(param)
    return

if __name__ == '__main__':   
    if len(sys.argv) < 3:
        # You can modify these values to test your code
        strategy = 'B'
        filename = 'example1.txt'
        param = "3"
    else:
        strategy = sys.argv[1]
        filename = sys.argv[2]
        param = sys.argv[3] if len(sys.argv) > 3 else None
    main(strategy, filename, int(param) if param else None)