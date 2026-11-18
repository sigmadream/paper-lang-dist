import sys

def main():
    line = sys.stdin.readline()
    s = line.strip()
    n = 0
    if s:
        n = int(s)
    counts = [0] * (n + 1)
    for i in range(1, n + 1):
        counts[i] = counts[i // 2] + (i % 2)
    print(' '.join(map(str, counts)))

if __name__ == '__main__':
    main()