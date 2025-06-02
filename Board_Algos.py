import matplotlib.pyplot as plt
import random
import math

class DFSNQueens:
    def solve(self, n):
        def is_safe(position, row, col):
            for r in range(row):
                c = position[r]
                if c == col or abs(c - col) == abs(r - row):
                    return False
            return True

        def dfs(position, row):
            if row == n:
                return position[:]
            for col in range(n):
                if is_safe(position, row, col):
                    position[row] = col
                    result = dfs(position, row + 1)
                    if result:
                        return result
            return None

        return dfs([0] * n, 0)

class HillClimbingNQueens:
    def solve(self, n):
        def compute_conflicts(board):
            conflicts = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                        conflicts += 1
            return conflicts

        def get_neighbors(board):
            neighbors = []
            for row in range(n):
                for col in range(n):
                    if board[row] != col:
                        new_board = board[:]
                        new_board[row] = col
                        neighbors.append(new_board)
            return neighbors

        board = [random.randint(0, n - 1) for _ in range(n)]
        current = board
        current_conflicts = compute_conflicts(current)
        while True:
            neighbors = get_neighbors(current)
            neighbor = min(neighbors, key=compute_conflicts)
            neighbor_conflicts = compute_conflicts(neighbor)
            if neighbor_conflicts >= current_conflicts:
                break
            current, current_conflicts = neighbor, neighbor_conflicts
            if current_conflicts == 0:
                break
        return current if compute_conflicts(current) == 0 else None

class SimulatedAnnealingNQueens:
    def solve(self, n):
        def compute_conflicts(board):
            conflicts = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                        conflicts += 1
            return conflicts

        board = [random.randint(0, n - 1) for _ in range(n)]
        temp = 100.0
        cooling = 0.95
        while temp > 1e-3:
            i = random.randint(0, n - 1)
            new_board = board[:]
            new_board[i] = random.randint(0, n - 1)
            delta = compute_conflicts(new_board) - compute_conflicts(board)
            if delta < 0 or random.random() < math.exp(-delta / temp):
                board = new_board
            temp *= cooling
            if compute_conflicts(board) == 0:
                return board
        return board if compute_conflicts(board) == 0 else None

class GeneticNQueens:
    def solve(self, n):
        def fitness(board):
            non_attacking = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if board[i] != board[j] and abs(board[i] - board[j]) != abs(i - j):
                        non_attacking += 1
            return non_attacking

        def crossover(p1, p2):
            point = random.randint(0, n - 1)
            child = p1[:point] + p2[point:]
            return child

        def mutate(board):
            board[random.randint(0, n - 1)] = random.randint(0, n - 1)
            return board

        population = [[random.randint(0, n - 1) for _ in range(n)] for _ in range(100)]
        for generation in range(1000):
            population = sorted(population, key=lambda x: -fitness(x))
            if fitness(population[0]) == n * (n - 1) // 2:
                return population[0]
            next_gen = population[:20]
            while len(next_gen) < 100:
                p1, p2 = random.choices(population[:50], k=2)
                child = mutate(crossover(p1, p2))
                next_gen.append(child)
            population = next_gen
        return population[0] if fitness(population[0]) == n * (n - 1) // 2 else None