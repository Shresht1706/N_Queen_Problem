import time
from Board_Algos import DFSNQueens, HillClimbingNQueens, SimulatedAnnealingNQueens, GeneticNQueens

def test_algorithm(algo_class, n, runs):
    total_time = 0
    success_count = 0
    print(f"Testing {algo_class.__name__} for {n}-Queens with {runs} runs")

    for _ in range(runs):
        algo = algo_class()
        start = time.time()
        solution = algo.solve(n)
        end = time.time()
        total_time += (end - start)
        if solution is not None:
            success_count += 1

    average_time = total_time / runs
    success_rate = success_count / runs
    print(f"Average time: {average_time:.4f}s")
    print(f"Success rate: {success_rate*100:.0f}%")
    return average_time, success_rate

test_algorithm(GeneticNQueens, 100, 1)