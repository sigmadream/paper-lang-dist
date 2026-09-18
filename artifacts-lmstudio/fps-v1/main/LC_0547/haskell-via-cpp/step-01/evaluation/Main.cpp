#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int components(const vector<vector<int>>& graph, int n) {
    vector<bool> seen(n, false);
    int count = 0;
    for (int i = 0; i < n; ++i) {
        if (!seen[i]) {
            queue<int> q;
            q.push(i);
            while (!q.empty()) {
                int v = q.front();
                q.pop();
                if (!seen[v]) {
                    seen[v] = true;
                    for (int j = 0; j < n; ++j) {
                        if (graph[v][j] == 1 && !seen[j]) {
                            q.push(j);
                        }
                    }
                }
            }
            count++;
        }
    }
    return count;
}

int main() {
    int n;
    cin >> n;
    vector<vector<int>> graph(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> graph[i][j];
        }
    }
    cout << components(graph, n) << endl;
    return 0;
}