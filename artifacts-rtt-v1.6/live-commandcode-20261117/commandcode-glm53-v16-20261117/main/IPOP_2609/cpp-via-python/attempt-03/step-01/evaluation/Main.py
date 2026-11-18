import sys

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    a, b = int(data[0]), int(data[1])
    g = gcd(a, b)
    print(g)
    print((a // g) * b)

main()