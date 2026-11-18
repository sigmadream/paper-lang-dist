#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n)) return 0;
    cin >> m;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    vector<int> dist(n + 1, -1);
    queue<int> q;
    dist[1] = 0;
    q.push(1);

    while (!q.empty()) {
        int v = q.front();
        q.pop();

        if (dist[v] >= 2) continue;

        for (int next : adj[v]) {
            if (dist[next] == -1) {
                dist[next] = dist[v] + 1;
                q.push(next);
            }
        }
    }

    int answer = 0;
    for (int i = 2; i <= n; ++i) {
        if (dist[i] == 1 || dist[i] == 2) {
            ++answer;
        }
    }

    cout << answer << '\n';
    return 0;
}