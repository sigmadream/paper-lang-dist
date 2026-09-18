#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

int main() {
    int N, M;
    std::cin >> N >> M;

    std::vector<std::vector<int>> adj(N + 1);
    for (int i = 0; i < M; ++i) {
        int a, b;
        std::cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    std::queue<int> q;
    std::vector<bool> visited(N + 1, false);
    std::vector<int> distance(N + 1, -1);

    q.push(1);
    visited[1] = true;
    distance[1] = 0;

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                distance[v] = distance[u] + 1;
                q.push(v);
            }
        }
    }

    int count = 0;
    for (int i = 2; i <= N; ++i) {
        if (distance[i] == 1 || distance[i] == 2) {
            ++count;
        }
    }

    std::cout << count << std::endl;

    return 0;
}