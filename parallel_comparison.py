import time
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
import math


# Simulate a CPU-intensive task
def heavy_computation(n=100_000):
    result = 0
    for i in range(1, n):
        result += math.sqrt(i) * math.sin(i)
    return result


def run_sequential(num_tasks, complexity):
    print(" Running tasks sequentially")
    start = time.time()
    for i in range(num_tasks):
        heavy_computation(complexity)
        print(f" → Task {i+1}/{num_tasks} done (sequential)")
    return time.time() - start


def run_multiprocessing(num_tasks, complexity):
    print(" Running tasks using multiprocessing")
    start = time.time()
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(heavy_computation, complexity) for _ in range(num_tasks)]
        for i, f in enumerate(futures):
            f.result()
            print(f" → Task {i+1}/{num_tasks} done (multiprocessing)")
    return time.time() - start


def plot_results(sequential_time, multiprocessing_time):
    labels = ['Sequential', 'Multiprocessing']
    times = [sequential_time, multiprocessing_time]
    colors = ['orange', 'green']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, times, color=colors)
    plt.title("Execution Time: Sequential vs Multiprocessing", fontsize=14)
    plt.ylabel("Time (seconds)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 f"{t:.2f}s", ha='center', fontsize=12)

    speedup = sequential_time / multiprocessing_time if multiprocessing_time else 0
    plt.figtext(0.5, 0.01, f" Speedup Achieved: {speedup:.2f}x",
                ha='center', fontsize=11, color='gray')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    TASKS = 6
    COMPLEXITY = 100_000

    seq_time = run_sequential(TASKS, COMPLEXITY)
    mp_time = run_multiprocessing(TASKS, COMPLEXITY)

    print(f"\n Summary:")
    print(f"Sequential Time      : {seq_time:.2f}s")
    print(f"Multiprocessing Time : {mp_time:.2f}s")
    print(f"Speedup              : {seq_time / mp_time:.2f}x faster")

    plot_results(seq_time, mp_time)
