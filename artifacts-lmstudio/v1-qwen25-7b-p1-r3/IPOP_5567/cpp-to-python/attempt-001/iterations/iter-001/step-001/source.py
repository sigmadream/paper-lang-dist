from collections import deque

def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    index = 0
    n = int(data[index])
    index += 1
    m = int(data[index])
    index += 1

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[index])
        index += 1
        v = int(data[index])
        index += 1
        adj[u].append(v)
        adj[v].append(u)

    dist = [-1] * (n + 1)
    q = deque()
    q.append(1)
    dist[1] = 0

    ans = 0

    while q:
        curr = q.popleft()

        for next_node in adj[curr]:
            if dist[next_node] == -1:
                dist[next_node] = dist[curr] + 1
                q.append(next_node)
                if dist[next_node] <= 2:
                    ans += 1

    print(ans)

if __name__ == "__main__":
    main()
