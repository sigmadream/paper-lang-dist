#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<int> nums;
    int x;
    while (cin >> x) nums.push_back(x);

    if (nums.size() < 2) return 0;

    int N = nums[0];
    int M = nums[1];

    if (M < 0) return 0;
    if (nums.size() < static_cast<size_t>(2 + 2 * M)) return 0;

    vector<pair<int, int>> edges;
    edges.reserve(M);

    int maxv = max(1, N);
    size_t idx = 2;

    for (int i = 0; i < M; ++i) {
        int a = nums[idx++];
        int b = nums[idx++];
        edges.emplace_back(a, b);
        maxv = max(maxv, max(a, b));
    }

    vector<vector<int>> adj(maxv + 1);

    for (auto [a, b] : edges) {
        if (a >= 1 && a <= maxv && b >= 1 && b <= maxv) {
            adj[a].push_back(b);
            adj[b].push_back(a);
        }
    }

    vector<int> dist(maxv + 1, -1);
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

    for (int i = 2; i <= maxv; ++i) {
        if (dist[i] >= 1 && dist[i] <= 2) {
            ++ans;
        }
    }

    cout << ans << '\n';

    return 0;
}