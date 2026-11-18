#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;
    if (!(cin >> N >> M)) {
        return 0;
    }

    vector<vector<int>> adj(N + 1);

    for (int i = 0; i < M; ++i) {
        int a, b;
        if (!(cin >> a >> b)) {
            return 0;
        }
        if (a >= 1 && a <= N && b >= 1 && b <= N) {
            adj[a].push_back(b);
            adj[b].push_back(a);
        }
    }

    if (N < 1) {
        return 0;
    }

    vector<int> dist(N + 1, -1);
    queue<int> q;

    dist[1] = 0;
    q.push(1);

    while (!q.empty()) {
        int cur = q.front();
        q.pop();

        for (int nxt : adj[cur]) {
            if (dist[nxt] == -1) {
                dist[nxt] = dist[cur] + 1;
                q.push(nxt);
            }
        }
    }

    int answer = 0;
    for (int v = 2; v <= N; ++v) {
        if (dist[v] == 1 || dist[v] == 2) {
            ++answer;
        }
    }

    cout << answer << '\n';
    return 0;
}