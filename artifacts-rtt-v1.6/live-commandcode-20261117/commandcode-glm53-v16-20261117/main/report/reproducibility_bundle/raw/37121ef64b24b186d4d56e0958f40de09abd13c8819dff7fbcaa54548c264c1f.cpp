#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    set<int> invited;
    for (int y : adj[1]) {
        if (y == 1) continue;
        invited.insert(y);
        for (int z : adj[y]) {
            if (z != 1) invited.insert(z);
        }
    }
    cout << invited.size() << "\n";
    return 0;
}