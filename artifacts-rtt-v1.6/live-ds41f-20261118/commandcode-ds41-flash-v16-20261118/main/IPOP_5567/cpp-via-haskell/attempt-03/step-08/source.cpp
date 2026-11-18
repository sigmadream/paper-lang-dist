#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    int m;
    if (!(cin >> m)) return 0;

    if (n <= 0) {
        cout << 0 << '\n';
        return 0;
    }

    vector<vector<int>> adj(n + 1);

    for (int i = 0; i < m; ++i) {
        int a, b;
        if (!(cin >> a >> b)) break;
        if (a >= 1 && a <= n && b >= 1 && b <= n) {
            adj[a].push_back(b);
            adj[b].push_back(a);
        }
    }

    vector<int> dist(n + 1, -1);
    queue<pair<int, int>> q;

    dist[1] = 0;
    q.push({1, 0});

    while (!q.empty()) {
        auto [u, du] = q.front();
        q.pop();

        if (du >= 2) continue;

        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = du + 1;
                q.push({v, du + 1});
            }
        }
    }

    int answer = 0;
    for (int v = 2; v <= n; ++v) {
        if (dist[v] == 1 || dist[v] == 2) {
            ++answer;
        }
    }

    cout << answer << '\n';
    return 0;
}