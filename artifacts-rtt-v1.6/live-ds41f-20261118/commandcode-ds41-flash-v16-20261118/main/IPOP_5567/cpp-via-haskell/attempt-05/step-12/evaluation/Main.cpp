#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    if (n <= 0) {
        cout << 0 << '\n';
        return 0;
    }

    int m = 0;
    if (!(cin >> m)) m = 0;

    vector<vector<int>> adj(n + 1);
    int limit = max(0, m);

    for (int i = 0; i < limit; ++i) {
        int a, b;
        if (!(cin >> a >> b)) break;
        if (a >= 1 && a <= n && b >= 1 && b <= n) {
            adj[a].push_back(b);
            adj[b].push_back(a);
        }
    }

    vector<char> inL1(n + 1, false), inL2(n + 1, false);

    for (int v : adj[1]) {
        if (v != 1) inL1[v] = true;
    }

    for (int u = 1; u <= n; ++u) {
        if (!inL1[u]) continue;
        for (int v : adj[u]) {
            if (v != 1 && !inL1[v]) {
                inL2[v] = true;
            }
        }
    }

    int ans = 0;
    for (int i = 1; i <= n; ++i) {
        if (inL1[i] || inL2[i]) ++ans;
    }

    cout << ans << '\n';
    return 0;
}