#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n)) return 0;
    if (!(cin >> m)) return 0;

    if (n <= 0) {
        cout << 0 << '\n';
        return 0;
    }

    vector<vector<int>> adj(n);
    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;
        --a;
        --b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    unordered_set<int> d1;
    for (int v : adj[0]) d1.insert(v);

    unordered_set<int> d2;
    for (int v : d1) {
        for (int w : adj[v]) {
            if (w != 0 && !d1.count(w)) {
                d2.insert(w);
            }
        }
    }

    cout << d1.size() + d2.size() << '\n';
    return 0;
}