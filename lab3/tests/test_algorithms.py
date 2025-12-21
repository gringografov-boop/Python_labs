import unittest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.algorithms import *

class TestFactorial(unittest.TestCase):
    def test_factorial_5(self):
        self.assertEqual(factorial(5), 120)
    def test_factorial_rec(self):
        self.assertEqual(factorial_recursive(5), 120)

class TestFibonacci(unittest.TestCase):
    def test_fibo_5(self):
        self.assertEqual(fibo(5), 5)
    def test_fibo_rec(self):
        self.assertEqual(fibo_recursive(5), 5)

class TestSortingFunctions(unittest.TestCase):
    def setUp(self):
        self.arr = [5, 2, 8, 1, 9]
        self.expected = [1, 2, 5, 8, 9]
    def test_bubble(self):
        self.assertEqual(bubble_sort(self.arr), self.expected)
    def test_quick(self):
        self.assertEqual(quick_sort(self.arr), self.expected)
    def test_heap(self):
        self.assertEqual(heap_sort(self.arr), self.expected)

class TestStack(unittest.TestCase):
    def test_basic(self):
        s = Stack()
        s.push(5)
        s.push(10)
        self.assertEqual(s.peek(), 10)
        self.assertEqual(s.pop(), 10)
        self.assertEqual(len(s), 1)
    def test_min(self):
        s = Stack()
        s.push(3)
        s.push(1)
        self.assertEqual(s.min(), 1)

class TestQueue(unittest.TestCase):
    def test_basic(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.front(), 1)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(len(q), 1)

if __name__ == "__main__":
    unittest.main()
