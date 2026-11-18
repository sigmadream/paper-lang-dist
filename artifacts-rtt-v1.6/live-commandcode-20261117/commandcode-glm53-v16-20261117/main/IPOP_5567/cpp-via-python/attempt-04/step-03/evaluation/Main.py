import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    m = int(data[1]) if len(data) > 1 else 0
    adj = [[] for _ in range(n + 1)]
    idx = 2
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
    dist = [-1] * (n + 1)
    if n >= 1:
        dist[1] = 0
    q = deque([1])
    ans = 0
    while q:
        curr = q.popleft()
        for nxt in adj[curr]:
            if dist[nxt] == -1:
                dist[nxt] = dist[curr] + 1
                q.append(nxt)
                if dist[nxt] <= 2:
                    ans += 1
    print(ans)

main()