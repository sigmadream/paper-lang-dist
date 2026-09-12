def gcd(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

def main():
    a, b = map(int, input().split())
    g = gcd(a, b)
    print(g)
    print((a // g) * b)

if __name__ == "__main__":
    main()
