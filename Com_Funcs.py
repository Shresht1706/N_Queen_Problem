import random
import time


def compute_conflicts(board, n):
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def test_algorithm(algo_class, runs, n):
    total_time = 0
    success_count = 0
    print(f"Testing {algo_class.__name__} for {n}-Queens with {runs} runs")

    for _ in range(runs):
        start = time.time()
        solution = algo_class.solve(n)
        end = time.time()
        total_time += (end - start)
        if solution is not None:
            success_count += 1

    average_time = total_time / runs
    success_rate = success_count / runs
    print(f"Average time: {average_time:.4f}s")
    if runs > 1:
        print(f"Success rate: {success_rate*100:.0f}%")
    return average_time, success_rate
