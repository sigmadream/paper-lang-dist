import sys

n, m, *values = map(int, sys.stdin.buffer.read().split())
graph = [set() for _ in range(n + 1)]
for a, b in zip(values[::2], values[1::2]):
    graph[a].add(b)
    graph[b].add(a)
invited = set(graph[1])
for friend in graph[1]:
    invited.update(graph[friend])
invited.discard(1)
print(len(invited))
