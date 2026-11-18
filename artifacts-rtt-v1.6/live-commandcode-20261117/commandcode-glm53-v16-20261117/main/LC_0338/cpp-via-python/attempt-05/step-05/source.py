import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0]) if data else 0
    counts = [0] * (n + 1)
    for i in range(1, n + 1):
        counts[i] = counts[i // 2] + (i % 2)
    print(' '.join(map(str, counts)))

if __name__ == "__main__":
    main()