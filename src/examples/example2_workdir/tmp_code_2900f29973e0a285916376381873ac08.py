def fib(n):
    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
    return a if n else b

fib_number = fib(14)
print("The 14th Fibonacci number is:", fib_number)