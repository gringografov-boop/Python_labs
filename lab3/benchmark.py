from src.algorithms import (
    bubble_sort,
    quick_sort,
    heap_sort,
    rand_int_array,
    nearly_sorted,
    many_duplicates,
    benchmark
)

def benchmmark_run():
    arrays = {
        "Random (100)":    rand_int_array(100, 0, 1000, seed=42),
        "Nearly sorted":   nearly_sorted(100, 5, seed=42),
        "Many duplicates": many_duplicates(100, k=10, seed=42),
    }

    algos = {
        "Bubble": bubble_sort,
        "Quick":  quick_sort,
        "Heap":   heap_sort,
    }

    results = benchmark(arrays, algos)

    for array_name, timings in results.items():
        print(f"{array_name}:")
        for algo_name, t in timings.items():
            print(f"  {algo_name}: {t * 1000:.4f} ms")


if __name__ == "__main__":
    benchmmark_run()
