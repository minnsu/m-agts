fib_sequence = [0, 1]
for i in range(2, 15):
    next_number = fib_sequence[i-1] + fib_sequence[i-2]
    fib_sequence.append(next_number)
print(f"The 14th Fibonacci number is: {fib_sequence[-2]}")