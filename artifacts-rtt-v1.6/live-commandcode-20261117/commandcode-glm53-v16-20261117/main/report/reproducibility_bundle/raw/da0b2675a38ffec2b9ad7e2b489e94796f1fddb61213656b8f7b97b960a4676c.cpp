#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    vector<char> dist(n + 1, 3);
    dist[1] = 0;
    set<int> d1, d2;
    for (int v : adj[1]) {
        if (v != 1) d1.insert(v);
        dist[v] = min(dist[v], (char)1);
    }
    for (int v : d1) {
        for (int w : adj[v]) {
            if (w != 1) d2.insert(w);
        }
    }
    set<int> ans;
    ans.insert(d1.begin(), d1.end());
    ans.insert(d2.begin(), d2.end());
    ans.erase(1);
    cout << ans.size() << "\n";
    return 0;
}