import numpy as np
import copy

class EightPuzzle:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def find_position(self, state, value):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == value:
                    return i, j

    def manhattan_distance(self, state):
        """Heuristic: Manhattan Distance"""
        distance = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != 0:  # Ignore the empty tile
                    x, y = self.find_position(self.goal, state[i][j])
                    distance += abs(i - x) + abs(j - y)
        return distance

    def misplaced_tiles(self, state):
        """Heuristic: Number of misplaced tiles"""
        count = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != 0 and state[i][j] != self.goal[i][j]:
                    count += 1
        return count

    def get_neighbors(self, state):
        """Generate all possible states from the current state"""
        neighbors = []
        x, y = self.find_position(state, 0)  # Find the empty tile
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append(new_state)
        return neighbors

    def hill_climbing(self, heuristic="manhattan"):
        """Hill Climbing Algorithm"""
        current_state = self.initial
        current_cost = self.manhattan_distance(current_state) if heuristic == "manhattan" else self.misplaced_tiles(current_state)
        steps = [current_state]

        while current_cost > 0:
            neighbors = self.get_neighbors(current_state)
            next_state = None
            next_cost = float('inf')
            
            for neighbor in neighbors:
                cost = self.manhattan_distance(neighbor) if heuristic == "manhattan" else self.misplaced_tiles(neighbor)
                if cost < next_cost:
                    next_cost = cost
                    next_state = neighbor

            if next_cost >= current_cost:  # No improvement, stuck in local maxima or plateau
                break

            current_state = next_state
            current_cost = next_cost
            steps.append(current_state)

        return steps, current_cost == 0

# Example configuration
initial_state = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]
goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Instantiate the puzzle
puzzle = EightPuzzle(initial_state, goal_state)

# Solve using Hill Climbing with Manhattan distance
steps, success = puzzle.hill_climbing(heuristic="manhattan")

# Output the solution
print("Initial State:")
print(np.array(initial_state))
print("\nSteps to Goal:")
for step in steps:
    print(np.array(step), "\n")
print("Success:", success)
