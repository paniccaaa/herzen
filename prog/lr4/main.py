# Задание 1 - Реализация обычная

def fib(n):
    result = []
    a, b = 0, 1
    while a <= n:
        result.append(a)
        a, b = b, a + b
    return result

# Задание 2 - Реализация с дополнительным классом FibonacchiLst

class FibonacchiLst:
    def __init__(self, lst):
        self.lst = lst
        self.fib_set = set(fib(max(lst)))  # Все числа фибоначчи до максимума в списке
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.lst):
            val = self.lst[self.index]
            self.index += 1
            if val in self.fib_set:
                return val
        raise StopIteration

# Пример использования:
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
fib_iterator = FibonacchiLst(lst)
print(list(fib_iterator))  # [0, 1, 2, 3, 5, 8, 1]

# Задание 3 - Реализация с помощью itertools

from itertools import islice

def fib_iter(iterable):
    max_val = max(iterable)
    fib_sequence = fib(max_val)
    return [x for x in iterable if x in fib_sequence]

# Пример использования:
l = list(range(14))
print(fib_iter(l))  # [0, 1, 1, 2, 3, 5, 8, 13]

# Реализация через декоратор

# import functools

# def fibonacci_gen():
#     a, b = 0, 1
#     while True:
#         yield a
#         a, b = b, a + b

# def coroutine(g):
#     @functools.wraps(g)
#     def wrapper(*args, **kwargs):
#         gen = g(*args, **kwargs)
#         next(gen) 
#         return gen
#     return wrapper

# @coroutine
# def my_gen():
#     gen = fibonacci_gen()
#     n = yield  
#     while True:
#         yield [next(gen) for _ in range(n)]
#         n = yield  

# gen = my_gen()
# print(gen.send(10))

# Задание 4 - реализация через генератор (yield)

def fibonacci_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b 

# Теперь my_gen - генератор 
def my_gen():
    gen = fibonacci_gen()
    n = (yield)  # wait for first value
    while True:
        yield [next(gen) for _ in range(n)]
        n = (yield)  # wait for the next value

gen = my_gen()
next(gen)  # init generator
print(gen.send(10))
