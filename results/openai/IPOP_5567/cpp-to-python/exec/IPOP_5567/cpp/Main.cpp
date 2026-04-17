#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<long long> data;
    long long x;
    while (cin >> x) data.push_back(x);

    if (data.size() < 2) return 0;

    size_t idx = 0;
    int n = (int)data[idx++];
    int m = (int)data[idx++];

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m && idx + 1 < data.size(); ++i) {
        int u = (int)data[idx++];
        int v = (int)data[idx++];
        if (u >= 0 && u <= n && v >= 0 && v <= n) {
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    vector<int> dist(n + 1, -1);
    deque<int> q;
    q.push_back(1);
    if (1 >= 0 && 1 <= n) dist[1] = 0;
    int ans = 0;

    while (!q.empty()) {
        int curr = q.front();
        q.pop_front();
        for (int nxt : adj[curr]) {
            if (dist[nxt] == -1) {
                dist[nxt] = dist[curr] + 1;
                q.push_back(nxt);
                if (dist[nxt] <= 2) {
                    ans += 1;
                }
            }
        }
    }

    cout << ans << '\n';
    return 0;
}
