import sys

global treasures
global n, m, grid, start, visited, heuristics, teleports

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
                teleports[ord(grid[i][j]) - ord('0')] = (i, j)

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
        heuristics[teleports[i][0]][teleports[i][1]] = heuristics[teleports[i + 1][0]][teleports[i + 1][1]]
    
def BFS():
    pass

def UCS():
    pass

def IDS():
    pass

def Greedy():
    pass

def A_star():
    pass

def Beam():
    pass


def main(strategy, filename):
    read_input(filename)
    print(grid)
    calculate_heuristics()
    print(heuristics)
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
        strategy = 'B'
        filename = 'example2.txt'
    else:
        strategy = sys.argv[1]
        filename = sys.argv[2]
    main(strategy, filename)