#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;
    if (!(cin >> N)) return 0;
    cin >> M;

    vector<vector<int>> graph(N + 1);
    for (int i = 0; i < M; ++i) {
        int a, b;
        cin >> a >> b;
        if (a >= 1 && a <= N && b >= 1 && b <= N) {
            graph[a].push_back(b);
            graph[b].push_back(a);
        }
    }

    vector<int> dist(N + 1, -1);
    queue<int> q;
    dist[1] = 0;
    q.push(1);

    while (!q.empty()) {
        int v = q.front();
        q.pop();

        if (dist[v] == 2) continue;

        for (int nxt : graph[v]) {
            if (dist[nxt] == -1) {
                dist[nxt] = dist[v] + 1;
                q.push(nxt);
            }
        }
    }

    int answer = 0;
    for (int v = 2; v <= N; ++v) {
        if (dist[v] == 1 || dist[v] == 2) ++answer;
    }

    cout << answer << '\n';
    return 0;
}