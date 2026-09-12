#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    int n, m;
    cin >> n >> m;

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

    int ans = 0;

    while (!q.empty()) {
        int curr = q.front();
        q.pop();

        for (int next_node : adj[curr]) {
            if (dist[next_node] == -1) {
                dist[next_node] = dist[curr] + 1;
                q.push(next_node);
                if (dist[next_node] <= 2) {
                    ans += 1;
                }
            }
        }
    }

    cout << ans << endl;

    return 0;
}
