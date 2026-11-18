import sys

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return

    m = int(data[0])
    n = int(data[1])

    total = m + n - 2
    k = min(m - 1, n - 1)

    result = 1
    for i in range(1, k + 1):
        result = result * (total - k + i) // i

    print(result)

if __name__ == "__main__":
    main()