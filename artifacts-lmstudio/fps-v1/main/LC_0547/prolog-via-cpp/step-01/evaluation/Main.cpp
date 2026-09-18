#include <iostream>
#include <vector>
#include <queue>
using namespace std;

void visit(const vector<vector<int>>& rows, int v, vector<bool>& seen) {
    if (seen[v]) return;
    seen[v] = true;
    for (int j = 0; j < rows.size(); ++j) {
        if (rows[v][j] == 1 && !seen[j]) {
            visit(rows, j, seen);
        }
    }
}

int components(const vector<vector<int>>& rows) {
    int n = rows.size();
    vector<bool> seen(n, false);
    int count = 0;
    for (int i = 0; i < n; ++i) {
        if (!seen[i]) {
            visit(rows, i, seen);
            ++count;
        }
    }
    return count;
}

int main() {
    int n;
    cin >> n;
    vector<vector<int>> rows(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> rows[i][j];
        }
    }
    cout << components(rows) << endl;
    return 0;
}