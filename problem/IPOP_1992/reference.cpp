#include <iostream>
#include <vector>
#include <string>

using namespace std;

string solve(const vector<string>& grid, int r, int c, int size) {
    char first = grid[r][c];
    bool same = true;
    for (int i = r; i < r + size; i++) {
        for (int j = c; j < c + size; j++) {
            if (grid[i][j] != first) {
                same = false;
                break;
            }
        }
        if (!same) break;
    }
    
    if (same) return string(1, first);
    
    int half = size / 2;
    string tl = solve(grid, r, c, half);
    string tr = solve(grid, r, c + half, half);
    string bl = solve(grid, r + half, c, half);
    string br = solve(grid, r + half, c + half, half);
    
    return "(" + tl + tr + bl + br + ")";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<string> grid(n);
    for (int i = 0; i < n; i++) cin >> grid[i];
    cout << solve(grid, 0, 0, n) << "\n";
    return 0;
}
