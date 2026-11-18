#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;
    if (!(cin >> N >> M)) {
        cout << 0 << '\n';
        return 0;
    }

    vector<vector<int>> adj(N + 1);
    for (int i = 0; i < M; ++i) {
        int a, b;
        cin >> a >> b;
        if (a >= 1 && a <= N && b >= 1 && b <= N) {
            adj[a].push_back(b);
            adj[b].push_back(a);
        }
    }

    set<int> candidates;
    if (N >= 1) {
        for (int v : adj[1]) {
            candidates.insert(v);
            for (int u : adj[v]) {
                candidates.insert(u);
            }
        }
    }

    candidates.erase(1);
    cout << candidates.size() << '\n';

    return 0;
}