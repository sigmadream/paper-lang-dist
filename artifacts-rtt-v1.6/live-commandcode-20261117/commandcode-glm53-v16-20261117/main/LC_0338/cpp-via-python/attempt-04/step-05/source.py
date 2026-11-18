import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    counts = [0] * (n + 1)
    for i in range(1, n + 1):
        counts[i] = counts[i // 2] + (i % 2)
    print(' '.join(map(str, counts)))

main()