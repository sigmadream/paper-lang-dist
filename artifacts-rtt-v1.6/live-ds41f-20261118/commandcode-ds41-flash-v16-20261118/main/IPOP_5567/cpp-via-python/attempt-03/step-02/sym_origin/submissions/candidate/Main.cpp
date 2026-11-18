#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<int> data;
    int x;
    while (cin >> x) data.push_back(x);

    if (data.size() < 2) return 0;

    int n = data[0];
    int m = data[1];

    vector<vector<int>> adj(n + 1);

    int idx = 2;
    for (int i = 0; i < m && idx + 1 < (int)data.size(); ++i) {
        int a = data[idx++];
        int b = data[idx++];
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    vector<int> dist(n + 1, -1);
    queue<int> q;

    q.push(1);
    dist[1] = 0;

    int ans = 0;

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