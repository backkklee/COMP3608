import sys
from heapq import heappush, heappop

global treasures
global n, m, grid, start, heuristics, teleports
global directions
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

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
    print(f"<{strat}> Search Initiated")
    print(f"Expanded: {expanded}")
    if (not path):
        print("NO PATH FOUND!")
        return
    print(f"Path Found: {path}")
    print(f"Taking this path will cost: {cost} Willpower")

def BFS():
    pass

def UCS():
    pass

def IDS():
    pass

def Greedy():
    fringe = []
    expanded = []
    heappush(fringe, (0, start))
    finished = 0
    cost = -1
    while fringe:
        x, y = heappop(fringe)[1]
        expanded.append((x, y))
        cost += 1
        if grid[y][x] == 'X':
            finished = 1
            break
        elif grid[y][x] == 'M':
            cost += 1
        elif grid[y][x] == 'B':
            cost += 2
        elif grid[y][x].isnumeric() and ord(grid[y][x]) % 2 == 1:
            cost -= 1
            teleport_exit = teleports[ord(grid[y][x]) - ord('0') + 1]
            heappush(fringe, (0, teleport_exit))
            continue
        for dir in directions:
            new_x = x + dir[0]
            new_y = y + dir[1]
            if (new_x < 0 or new_x >= m or new_y < 0 or new_y >= n):
                continue
            if (new_x, new_y) in fringe or (new_x, new_y) in expanded:
                continue
            # If the cell is a wall, skip it
            if grid[new_y][new_x] == 'W':
                continue
            heappush(fringe, (heuristics[new_y][new_x], (new_x, new_y)))
    if not finished:
        output("Greedy", expanded, [], cost)
        return
    output("Greedy", expanded, expanded, cost)



def A_star():
    pass

def Beam():
    pass


def main(strategy, filename):
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
            IDS()
        case "G":
            Greedy()
        case "A":
            A_star()
        case "M":
            Beam()
    return

if __name__ == '__main__':   
    if len(sys.argv) < 3:
        # You can modify these values to test your code
        strategy = 'G'
        filename = 'example3.txt'
    else:
        strategy = sys.argv[1]
        filename = sys.argv[2]
    main(strategy, filename)