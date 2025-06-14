import random
import time
import tracemalloc
import os
import csv
from Com_Funcs import compute_conflicts,test_algorithm 

class HillClimbingNQueens:
    @classmethod
    def solve(cls, n, max_sideways=100, max_restarts=100, csv_file="HCNQ_Results.csv"):
        def get_neighbors(board):
            neighbors = []
            for row in range(n):
                for col in range(n):
                    if board[row] != col:
                        new_board = board[:]
                        new_board[row] = col
                        neighbors.append(new_board)
            return neighbors

        tracemalloc.start()
        start_time = time.time()
        print(f"Solving board for {n} Queens")

        for restart in range(max_restarts):
            board = [random.randint(0, n - 1) for _ in range(n)]
            current = board
            current_conflicts = compute_conflicts(current, n)
            steps = 0
            sideways_moves = 0

            while True:
                neighbors = get_neighbors(current)
                conflicts_list = [(compute_conflicts(nb, n), nb) for nb in neighbors]

                min_conf = min(conflicts_list, key=lambda x: x[0])[0]
                candidates = [nb for conf, nb in conflicts_list if conf == min_conf]

                if not candidates or min_conf > current_conflicts:
                    break  # Local minimum reached

                neighbor = random.choice(candidates)
                neighbor_conflicts = compute_conflicts(neighbor, n)

                if neighbor_conflicts == current_conflicts:
                    sideways_moves += 1
                    if sideways_moves > max_sideways:
                        break
                else:
                    sideways_moves = 0

                current = neighbor
                current_conflicts = neighbor_conflicts
                steps += 1

                if current_conflicts == 0:
                    break

            if current_conflicts == 0:
                print(f" Solved after {restart+1} restart(s)")
                break  

        end_time = time.time()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        time_taken = end_time - start_time
        process = psutil.Process(os.getpid())
        total_mem_kb = process.memory_info().rss / 1024

        cls.log_results(
            csv_file, n, steps, current_conflicts, time_taken,
            peak_mem / 1024, total_mem_kb
        )
        
        if current_conflicts % 1 == 0:
            print(f"Conflicts: {current_conflicts}")

        if current_conflicts == 0:
            print(f" Solved {n}-Queens in {steps} steps, {restart+1} restarts, {time_taken:.2f}s")
            return current
        else:
            print(f" Failed after {max_restarts} restarts. Conflicts: {current_conflicts}")
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
            



# Example usage:
HillClimbingNQueens.solve(200)