import random
import tracemalloc
import csv
import os
import psutil
import time
from Com_Funcs import test_algorithm  # visualize_board omitted for performance

class GeneticNQueens:
    @classmethod
    def solve(cls, n, max_generations=50000, csv_file='GNQ_Results.csv'):
        population_size = n * 10
        elite_size = max(1, population_size // 10)
        tournament_size = max(2, population_size // 4)
        max_fitness = n * (n - 1) // 2      #

        print(f"\nSolving {n}-Queens using Advanced Genetic Algorithm", flush=True)
        print(f"Population: {population_size}, Elite: {elite_size}, Tournament: {tournament_size}", flush=True)
        print(f"The Max Fitness to be achieved is: {max_fitness}", flush=True)

        tracemalloc.start()
        start_time = time.time()

        def fitness(board):
            attacking = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                        attacking += 1
            return max_fitness - attacking

        def crossover(p1, p2):
            point = random.randint(1, n - 2)
            child = p1[:point] + [gene for gene in p2 if gene not in p1[:point]]
            return child if len(child) == n else p1

        def mutate(board, mutation_rate=0.1):
            board = board[:]
            if random.random() < mutation_rate:
                i, j = random.sample(range(n), 2)
                board[i], board[j] = board[j], board[i]
            return board

        population = [random.sample(range(n), n) for _ in range(population_size)]
        population = [(board, fitness(board)) for board in population]

        generation = 0
        best_board, best_fitness = max(population, key=lambda x: x[1])

        while generation < max_generations:
            generation += 1

            population.sort(key=lambda x: -x[1])
            best_board, best_fitness = population[0]

            if generation % 1 == 0 or best_fitness == max_fitness:
                print(f"Generation {generation}: Best fitness = {best_fitness}", flush=True)

            if best_fitness == max_fitness:
                print(f"\n Solution found in generation {generation}!", flush=True)
                break

            next_gen = population[:elite_size]

            while len(next_gen) < population_size:
                contenders = random.sample(population[:tournament_size], 2)
                p1, p2 = contenders[0][0], contenders[1][0]
                child = mutate(crossover(p1, p2))
                next_gen.append((child, fitness(child)))

            population = next_gen

        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.time()
        time_taken = end_time - start_time

        process = psutil.Process(os.getpid())
        total_mem_kb = process.memory_info().rss / 1024

        cls.log_results(csv_file, n, generation, population_size, elite_size,
                        tournament_size, best_fitness, time_taken,
                        peak_mem / 1024, total_mem_kb)

        return best_board

    @staticmethod
    def log_results(csv_file, n, generations, population, elite, tournament, fitness, time_taken, peak_memory_kb, total_memory_kb):
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                n, generations, population, elite, tournament,
                fitness, f"{time_taken:.2f}", f"{peak_memory_kb:.2f}", f"{total_memory_kb:.2f}"
            ])


test_algorithm(GeneticNQueens,10,30)
