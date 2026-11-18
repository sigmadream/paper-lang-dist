#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n)) return 0;
    if (!(cin >> m)) return 0;

    if (n <= 0) {
        cout << 0 << '\n';
        return 0;
    }

    vector<vector<int>> adj(n + 1);

    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<int> dist(n + 1, -1);
    queue<int> q;

    q.push(1);
    dist[1] = 0;

    int answer = 0;

    while (!q.empty()) {
        int current = q.front();
        q.pop();

        for (int next : adj[current]) {
            if (dist[next] == -1) {
                dist[next] = dist[current] + 1;
                q.push(next);

                if (dist[next] <= 2) {
                    ++answer;
                }
            }
        }
    }

    cout << answer << '\n';
    return 0;
}