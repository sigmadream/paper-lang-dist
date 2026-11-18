import sys, math

def main():
    data = sys.stdin.read().split()
    a, b = int(data[0]), int(data[1])
    g = math.gcd(a, b)
    print(g)
    print((a // g) * b)

main()