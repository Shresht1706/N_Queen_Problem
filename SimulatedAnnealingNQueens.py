import random
import math
import time
import tracemalloc
import psutil
import os
import csv
from Com_Funcs import compute_conflicts

class SimulatedAnnealingNQueens:
    @classmethod
    def solve(cls, n, max_steps=20000, csv_file="SANQ_Results.csv"):
        def random_board():
            return [random.randint(0, n - 1) for _ in range(n)]

        def get_conflicted_rows(board):
            conflicts = [0] * n
            for i in range(n):
                for j in range(n):
                    if i != j and (board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j)):
                        conflicts[i] += 1
            return conflicts

        tracemalloc.start()
        start_time = time.time()

        board = random_board()
        temp = 100.0
        cooling_rate = 0.99
        min_temp = 1e-4
        steps = 0

        while temp > min_temp and steps < max_steps:
            conflicts = get_conflicted_rows(board)
            max_conflict = max(conflicts)
            if max_conflict == 0:
                break

            conflict_rows = [i for i, val in enumerate(conflicts) if val == max_conflict]
            row = random.choice(conflict_rows)

            current_col = board[row]
            min_conflicts = compute_conflicts(board, n)
            best_col = current_col

            for col in range(n):
                if col != current_col:
                    board[row] = col
                    conf = compute_conflicts(board, n)
                    if conf < min_conflicts:
                        min_conflicts = conf
                        best_col = col
            
            board[row] = best_col if best_col != current_col else random.randint(0, n - 1)

            new_conflicts = compute_conflicts(board, n)
            delta = new_conflicts - min_conflicts

            if delta > 0 and random.random() >= math.exp(-delta / temp):
                board[row] = current_col  # reject the worse move

            temp *= cooling_rate
            steps += 1

        end_time = time.time()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        time_taken = end_time - start_time
        process = psutil.Process(os.getpid())
        total_mem_kb = process.memory_info().rss / 1024
        final_conflicts = compute_conflicts(board, n)

        cls.log_results(csv_file, n, steps, final_conflicts, time_taken,
                        peak_mem / 1024, total_mem_kb)

        if final_conflicts == 0:
            print(f"Solved {n}-Queens in {steps} steps and {time_taken:.2f} seconds")
            return board
        else:
            print(f"Stopped at {final_conflicts} conflicts after {steps} steps and {time_taken:.2f} seconds")
            return None

    @staticmethod
    def log_results(csv_file, n, steps, conflicts, time_taken, peak_memory_kb, total_memory_kb):
        file_exists = os.path.exists(csv_file)
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow([
                    "N", "Steps", "Conflicts", "Time (s)",
                    "Peak Memory (KB)", "Total Memory (KB)"
                ])
            writer.writerow([
                n, steps, conflicts, f"{time_taken:.2f}",
                f"{peak_memory_kb:.2f}", f"{total_memory_kb:.2f}"
            ])

if __name__ == "__main__":
    solver = SimulatedAnnealingNQueens
    result = solver.solve(30)
    print(result)
