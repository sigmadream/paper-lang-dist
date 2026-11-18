#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<int> nums;
    int x;
    while (cin >> x) nums.push_back(x);

    if (nums.empty()) return 0;
    int n = nums[0];

    if (nums.size() < 2) return 0;
    int m = nums[1];

    if (n <= 0) {
        cout << 0 << '\n';
        return 0;
    }

    vector<vector<int>> adj(n + 1);
    int idx = 2;
    for (int i = 0; i < m && idx + 1 < (int)nums.size(); ++i, idx += 2) {
        int a = nums[idx];
        int b = nums[idx + 1];
        if (a >= 1 && a <= n && b >= 1 && b <= n) {
            adj[a].push_back(b);
            adj[b].push_back(a);
        }
    }

    vector<int> dist(n + 1, -1);
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

    int answer = 0;
    for (int i = 2; i <= n; ++i) {
        if (dist[i] == 1 || dist[i] == 2) ++answer;
    }

    cout << answer << '\n';
    return 0;
}