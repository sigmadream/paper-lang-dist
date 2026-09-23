#include <iostream>
#include <vector>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) {
        return 0;
    }

    vector<vector<int>> g(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> g[i][j];
        }
    }

    vector<bool> seen(n, false);
    int components = 0;
    for (int i = 0; i < n; ++i) {
        if (!seen[i]) {
            ++components;
            vector<int> stack_nodes;
            stack_nodes.push_back(i);
            seen[i] = true;
            while (!stack_nodes.empty()) {
                int u = stack_nodes.back();
                stack_nodes.pop_back();
                for (int v = 0; v < n; ++v) {
                    if (g[u][v] && !seen[v]) {
                        seen[v] = true;
                        stack_nodes.push_back(v);
                    }
                }
            }
        }
    }

    cout << components << "\n";
    return 0;
}
