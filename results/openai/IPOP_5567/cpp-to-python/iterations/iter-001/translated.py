import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if len(data) < 2:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    dist = [-1] * (n + 1)
    q = deque([1])
    dist[1] = 0
    ans = 0

    while q:
        curr = q.popleft()
        for nxt in adj[curr]:
            if dist[nxt] == -1:
                dist[nxt] = dist[curr] + 1
                q.append(nxt)
                if dist[nxt] <= 2:
                    ans += 1

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()
