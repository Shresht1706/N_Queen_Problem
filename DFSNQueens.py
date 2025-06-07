import random
import math
from Com_Funcs import test_algorithm, visualize_board
import tracemalloc
import csv
import os
import psutil
import time

class DFSNQueens:
    @classmethod
    def solve(cls, n, csv_file='DFSNQ_Results.csv'):
        cls.recursive_calls = 0  # Track number of dfs calls

        def is_safe(position, row, col):
            for r in range(row):
                c = position[r]
                if c == col or abs(c - col) == abs(r - row):
                    return False
            return True

        def dfs(position, row):
            cls.recursive_calls += 1
            if row == n:
                return position[:]
            for col in range(n):
                if is_safe(position, row, col):
                    position[row] = col
                    result = dfs(position, row + 1)
                    if result:
                        return result
            return None

        print(f"\nSolving {n}-Queens using DFS Backtracking")
        tracemalloc.start()
        start_time = time.time()

        solution = dfs([0] * n, 0)

        end_time = time.time()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        process = psutil.Process(os.getpid())
        total_mem_kb = process.memory_info().rss / 1024

        time_taken = end_time - start_time

        # Log results in CSV
        cls.log_results(csv_file, n, cls.recursive_calls, time_taken, peak_mem / 1024, total_mem_kb)

        if solution:
            print(f"Solution found with {cls.recursive_calls} recursive calls")
            print(f"Time taken: {time_taken:.4f} seconds")
            print(f"Peak memory usage: {peak_mem / 1024:.2f} KB")
            print(f"Total memory usage: {total_mem_kb:.2f} KB")
        else:
            print("No solution found")

        return solution

    @staticmethod
    def log_results(csv_file, n, recursive_calls, time_taken, peak_memory_kb, total_memory_kb):
        file_exists = os.path.exists(csv_file)
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['N', 'Recursive Calls', 'Time (s)', 'Peak Memory (KB)', 'Total Memory (KB)'])
            writer.writerow([n, recursive_calls, f"{time_taken:.4f}", f"{peak_memory_kb:.2f}", f"{total_memory_kb:.2f}"])

test_algorithm(DFSNQueens, 10, 30)