#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<int> data;
    int x;
    while (cin >> x) data.push_back(x);

    if (data.empty()) return 0;

    size_t idx = 0;
    int n = data[idx++];

    if (idx >= data.size()) return 0;

    int m = data[idx++];

    vector<vector<int>> adj(n + 1);

    for (int i = 0; i < m; ++i) {
        if (idx + 1 >= data.size()) break;

        int u = data[idx++];
        int v = data[idx++];

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<int> dist(n + 1, -1);
    queue<int> q;
    int ans = 0;

    if (n >= 1) {
        dist[1] = 0;
        q.push(1);
    }

    while (!q.empty()) {
        int curr = q.front();
        q.pop();

        for (int nxt : adj[curr]) {
            if (dist[nxt] == -1) {
                dist[nxt] = dist[curr] + 1;
                q.push(nxt);

                if (dist[nxt] <= 2) {
                    ++ans;
                }
            }
        }
    }

    cout << ans << '\n';

    return 0;
}