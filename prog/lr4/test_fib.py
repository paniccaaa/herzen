import pytest
from main import *

def test_fib():
    assert fib(1) == [0, 1, 1], "Тест для n = 1 не пройден"
    assert fib(2) == [0, 1, 1, 2], "Тест для n = 2 не пройден"
    assert fib(5) == [0, 1, 1, 2, 3, 5], "Тест для n = 5 не пройден"
    assert fib(0) == [0], "Тест для n = 0 не пройден"
    assert fib(10) == [0, 1, 1, 2, 3, 5, 8], "Тест для n = 10 не пройден"

def test_fibonacchi_lst():
    lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    fib_iterator = FibonacchiLst(lst)
    assert list(fib_iterator) == [0, 1, 2, 3, 5, 8, 1], "Тест для FibonacchiLst не пройден"

    lst2 = [13, 21, 22, 34, 35, 55]
    fib_iterator2 = FibonacchiLst(lst2)
    assert list(fib_iterator2) == [13, 21, 34, 55], "Тест для FibonacchiLst c другими числами не пройден"

    lst3 = [4, 6, 7, 9]  # Список не содержит чисел Фибоначчи
    fib_iterator3 = FibonacchiLst(lst3)
    assert list(fib_iterator3) == [], "Тест для списка без чисел Фибоначчи не пройден"

def fib_iter(iterable):
    fib_sequence = fib(max(iterable))
    return [x for x in iterable if x in fib_sequence]

def test_my_gen():
    gen = my_gen()
    next(gen)  # Инициализируем генератор
    assert gen.send(5) == [0, 1, 1, 2, 3], "Тест для my_gen с n = 5 не пройден"
    next(gen)  # Необходимо вызывать next после отправки каждого значения
    assert gen.send(3) == [5, 8, 13], "Тест для my_gen с n = 3 не пройден"
