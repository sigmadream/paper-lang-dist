#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;
    if (!(cin >> N >> M)) return 0;

    vector<vector<int>> adj(N + 1);

    for (int i = 0; i < M; ++i) {
        int a, b;
        if (!(cin >> a >> b)) break;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    vector<int> dist(N + 1, -1);
    queue<int> q;

    dist[1] = 0;
    q.push(1);

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        if (dist[u] == 2) continue;

        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }

    int ans = 0;
    for (int i = 2; i <= N; ++i) {
        if (dist[i] == 1 || dist[i] == 2) {
            ++ans;
        }
    }

    cout << ans << '\n';
    return 0;
}