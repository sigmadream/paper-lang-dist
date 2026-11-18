import sys
from collections import deque

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    idx = 0
    n = data[idx]
    idx += 1
    if idx >= len(data):
        return
    m = data[idx]
    idx += 1

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        if idx + 1 >= len(data):
            break
        u = data[idx]
        v = data[idx + 1]
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    dist = [-1] * (n + 1)
    q = deque()
    ans = 0

    if n >= 1:
        dist[1] = 0
        q.append(1)

    while q:
        curr = q.popleft()

        for nxt in adj[curr]:
            if dist[nxt] == -1:
                dist[nxt] = dist[curr] + 1
                q.append(nxt)

                if dist[nxt] <= 2:
                    ans += 1

    print(ans)

if __name__ == "__main__":
    main()