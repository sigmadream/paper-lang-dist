import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    a = [int(x) for x in tokens[1:n + 1]]
    write_idx = 0
    for read_idx in range(n):
        if a[read_idx] != 0:
            a[write_idx], a[read_idx] = a[read_idx], a[write_idx]
            write_idx += 1
    sys.stdout.write(" ".join(map(str, a)) + "\n")

if __name__ == '__main__':
    main()
