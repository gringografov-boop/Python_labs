from src.algorithms import (
    factorial, factorial_recursive,
    fibo, fibo_recursive,
    bubble_sort, quick_sort, heap_sort, counting_sort, radix_sort, bucket_sort,
    Stack, Queue,
    rand_int_array, nearly_sorted, many_duplicates,
    benchmark,
)

def _show_menu():
    print("1. Факториал")
    print("2. Фибоначчи")
    print("3. Сортировки")
    print("4. Стек")
    print("5. Очередь")
    print("6. Бенчмарк")
    print("7. Тесты")
    print("0. Выход")

def _factorial_demo():
    n = int(input("n = "))
    print(f"factorial({n}) = {factorial(n)}")
    print(f"factorial_recursive({n}) = {factorial_recursive(n)}")

def _fibo_demo():
    n = int(input("n = "))
    print(f"fibo({n}) = {fibo(n)}")
    print(f"fibo_recursive({n}) = {fibo_recursive(n)}")

def _sorting_demo():
    arr = [int(x) for x in input().split()]
    print("Исходный:", arr)
    print("Bubble:", bubble_sort(arr))
    print("Quick:", quick_sort(arr))
    print("Heap:", heap_sort(arr))
    print("Counting:", counting_sort(arr))
    print("Radix:", radix_sort(arr))
    print("Bucket:", bucket_sort(arr))

def _stack_demo():
    stack = Stack()
    print("Вводите числа для добавления в стек (для выхода введите 'q'):")
    while True:
        user_input = input("push: ").strip()
        if user_input.lower() == 'q':
            break
        try:
            x = int(user_input)
            stack.push(x)
            print(f"  Добавили {x}, размер стека: {len(stack)}")
        except ValueError:
            print("  Ошибка: введите целое число")
    if stack.is_empty():
        print("Стек пуст")
        return
    print(f"Минимум в стеке: {stack.min()}")
    print("Удаляем элементы:")
    
    while not stack.is_empty():
        x = stack.pop()
        print(f"pop() → {x}, осталось: {len(stack)}")


def _queue_demo():
    queue = Queue()
    print("Вводите числа для добавления в очередь (для выхода введите 'q'):")
    
    while True:
        user_input = input("enqueue: ").strip()
        if user_input.lower() == 'q':
            break
        try:
            x = int(user_input)
            queue.enqueue(x)
            print(f"  Добавили {x}, размер очереди: {len(queue)}")
        except ValueError:
            print("  Ошибка: введите целое число")
    
    if queue.is_empty():
        print("Очередь пуста!")
        return
    
    print(f"\nПервый в очереди: {queue.front()}")
    print("\nУдаляем элементы:")
    
    while not queue.is_empty():
        x = queue.dequeue()
        print(f"  dequeue() → {x}, осталось: {len(queue)}")


def _benchmark_demo():
    print("\n--- Бенчмарк ---")
    
    # Выбираем размер массива
    try:
        n = int(input("Размер массива (n): "))
        if n <= 0:
            print("Ошибка: размер должен быть > 0")
            return
    except ValueError:
        print("Ошибка: введите целое число")
        return
    try:
        lo = int(input("Минимальное значение: "))
        hi = int(input("Максимальное значение: "))
        if lo >= hi:
            print("Ошибка: low должно быть < high")
            return
    except ValueError:
        print("Ошибка: введите целые числа")
        return
    print("\nДоступные сортировки:")
    print("1. Bubble")
    print("2. Quick")
    print("3. Counting")
    print("4. Radix")
    print("5. Heap")
    
    choices = input("Выберите номера (через запятую, например: 1,2,3): ").strip().split(',')
    
    algo_map = {
        '1': ("Bubble", bubble_sort),
        '2': ("Quick", quick_sort),
        '3': ("Counting", counting_sort),
        '4': ("Radix", radix_sort),
        '5': ("Heap", heap_sort),
    }
    
    algos = {}
    for choice in choices:
        choice = choice.strip()
        if choice in algo_map:
            name, func = algo_map[choice]
            algos[name] = func
    if not algos:
        print("Ошибка: не выбрана ни одна сортировка")
        return
    arrays = {
        "Random":     rand_int_array(n, lo, hi, seed=42),
        "Nearly":     nearly_sorted(n, max(1, n // 20), seed=42),
        "Duplicates": many_duplicates(n, k=max(2, n // 10), seed=42),
    }
    print(f"Тестирование {len(algos)} сортировок на {len(arrays)} типах массивов (n={n})...\n")
    
    results = benchmark(arrays, algos)
    
    for name, timings in results.items():
        print(f"\n{name}:")
        for algo, t in timings.items():
            print(f"  {algo}: {t * 1000:.4f} ms")
    
    # Вывести сравнение
    print("\n" + "="*50)
    print("ИТОГИ:")
    for algo_name in algos.keys():
        total_time = sum(results[arr_name][algo_name] for arr_name in arrays.keys())
        print(f"  {algo_name}: {total_time * 1000:.4f} ms (всего)")

def _tests_demo():
    import subprocess
    import sys
    import os
    
    here = os.path.dirname(__file__)
    tests_path = os.path.join(here, "tests", "test_algorithms.py")

    result = subprocess.run(
        [sys.executable, tests_path],
        capture_output=False
    )
    if result.returncode == 0:
        print("Все тесты прошли успешно!")
    else:
        print("Некоторые тесты не прошли.")

def run_cli():
    while True:
        _show_menu()
        choice = input("Выбор: ").strip()
        try:
            if choice == "1":
                _factorial_demo()
            elif choice == "2":
                _fibo_demo()
            elif choice == "3":
                _sorting_demo()
            elif choice == "4":
                _stack_demo()
            elif choice == "5":
                _queue_demo()
            elif choice == "6":
                _benchmark_demo()
            elif choice == "7":
                _tests_demo()
            elif choice == "0":
                print("Конец")
                break
            else:
                print("Ошибка: неверный выбор")
        except Exception as e:
            print("Ошибка:", e)
