def factorial(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def factorial_recursive(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n - 1)

def fibo(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a = 0
    b = 1
    for _ in range(2, n + 1):
        temp = a + b
        a = b
        b = temp
    return b

def fibo_recursive(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibo_recursive(n - 1) + fibo_recursive(n - 2)

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def counting_sort(arr):
    if not arr:
        return []
    min_val = min(arr)
    max_val = max(arr)
    count = [0] * (max_val - min_val + 1)
    for num in arr:
        count[num - min_val] += 1
    result = []
    for i in range(len(count)):
        for _ in range(count[i]):
            result.append(i + min_val)
    return result

def radix_sort(arr):
    if not arr:
        return []
    
    negative = [x for x in arr if x < 0]
    non_negative = [x for x in arr if x >= 0]
    
    sorted_non_negative = _radix_sort_positive(non_negative)
    abs_negative = [-x for x in negative]
    sorted_abs_negative = _radix_sort_positive(abs_negative)
    sorted_negative = [-x for x in reversed(sorted_abs_negative)]
    return sorted_negative + sorted_non_negative


def _radix_sort_positive(arr):
    if not arr:
        return []
    
    max_num = max(arr)
    exp = 1
    result = arr[:]
    
    while max_num // exp > 0:
        result = counting_by_digit(result, exp)
        exp *= 10
    
    return result


def counting_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    
    return output


def bucket_sort(arr):
    if not arr:
        return []
    n = len(arr)
    min_val = min(arr)
    max_val = max(arr)
    if min_val == max_val:
        return arr
    normalized = [(x - min_val) / (max_val - min_val) for x in arr]
    bucket_count = 10
    buckets = [[] for _ in range(bucket_count)]
    for x in normalized:
        idx = int(x * bucket_count)
        if idx == bucket_count:
            idx -= 1
        buckets[idx].append(x)
    for i in range(bucket_count):
        buckets[i] = bubble_sort(buckets[i])
    result = []
    for bucket in buckets:
        result.extend(bucket)
    return [x * (max_val - min_val) + min_val for x in result]

def heap_sort(arr):
    a = arr.copy()
    n = len(a)
    def heapify(size, i):
        largest = i
        left = 2*i + 1
        right = 2*i + 2
        if left < size and a[left] > a[largest]:
            largest = left
        if right < size and a[right] > a[largest]:
            largest = right
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            heapify(size, largest)
    for i in range(n//2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        heapify(i, 0)
    return a

# Стек
class Stack:
    def __init__(self):
        self.items = []
        self.min_stack = []
    def push(self, x):
        self.items.append(x)
        if not self.min_stack or x <= self.min_stack[-1]:
            self.min_stack.append(x)
    def pop(self):
        if not self.items:
            raise IndexError("pop from empty stack")
        x = self.items.pop()
        if x == self.min_stack[-1]:
            self.min_stack.pop()
        return x
    def peek(self):
        if not self.items:
            raise IndexError("peek from empty stack")
        return self.items[-1]
    def is_empty(self):
        return len(self.items) == 0
    def __len__(self):
        return len(self.items)
    def min(self):
        if not self.min_stack:
            raise IndexError("min from empty stack")
        return self.min_stack[-1]

# Очередь
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque() 
    
    def enqueue(self, x):
        self.items.append(x)
    def dequeue(self):
        if not self.items:
            raise IndexError("dequeue from empty queue")
        return self.items.popleft() 
    def front(self):
        if not self.items:
            raise IndexError("front from empty queue")
        return self.items[0]
    def is_empty(self):
        return len(self.items) == 0
    
    def __len__(self):
        return len(self.items)


# Генераторы
import random
def rand_int_array(n, lo, hi, seed=None):
    if seed is not None:
        random.seed(seed)
    return [random.randint(lo, hi) for _ in range(n)]

def nearly_sorted(n, swaps, seed=None):
    if seed is not None:
        random.seed(seed)
    arr = list(range(n))
    for _ in range(swaps):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def many_duplicates(n, k=5, seed=None):
    if seed is not None:
        random.seed(seed)
    return [random.randint(0, k - 1) for _ in range(n)]

def reverse_sorted(n):
    return list(range(n - 1, -1, -1))

def rand_float_array(n, seed=None):
    if seed is not None:
        random.seed(seed)
    return [random.random() for _ in range(n)]

# Бенчмарк
import time
def timeit(func, arr):
    start = time.time()
    func(arr)
    return time.time() - start

def benchmark(arrays, algos):
    results = {}
    for name, arr in arrays.items():
        results[name] = {}
        for algo_name, algo in algos.items():
            elapsed = timeit(algo, arr)
            results[name][algo_name] = elapsed
    return results
