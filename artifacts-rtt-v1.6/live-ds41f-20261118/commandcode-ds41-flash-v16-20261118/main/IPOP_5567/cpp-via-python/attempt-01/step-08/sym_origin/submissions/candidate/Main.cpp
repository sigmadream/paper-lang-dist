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

    size_t idx = 2;
    for (int i = 0; i < m; i++) {
        if (idx + 1 >= data.size()) break;
        int a = data[idx];
        int b = data[idx + 1];
        idx += 2;

        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    vector<int> dist(n + 1, -1);
    queue<int> q;

    if (n >= 1) {
        dist[1] = 0;
        q.push(1);
    }

    int answer = 0;

    while (!q.empty()) {
        int cur = q.front();
        q.pop();

        for (int nxt : adj[cur]) {
            if (dist[nxt] == -1) {
                dist[nxt] = dist[cur] + 1;
                q.push(nxt);

                if (dist[nxt] <= 2) {
                    answer++;
                }
            }
        }
    }

    cout << answer << '\n';

    return 0;
}