import sys

a, b = map(int, sys.stdin.buffer.read().split())
left, right = a, b
while right:
    left, right = right, left % right
print(left)
print(a // left * b)
