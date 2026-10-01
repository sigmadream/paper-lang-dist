import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    g = []
    for _ in range(n):
        row = [int(x) for x in tokens[idx:idx + n]]
        g.append(row)
        idx += n

    seen = [False] * n
    components = 0

    for i in range(n):
        if not seen[i]:
            components += 1
            stack = [i]
            seen[i] = True
            while stack:
                u = stack.pop()
                for v in range(n):
                    if g[u][v] and not seen[v]:
                        seen[v] = True
                        stack.append(v)

    print(components)

if __name__ == '__main__':
    main()
