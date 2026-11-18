#include <iostream>
#include <vector>
#include <string>
#include <cctype>

using namespace std;

int n;
int ans = 0;
vector<bool> col;
vector<bool> diag1;
vector<bool> diag2;

void solve(int r) {
    if (r == n) {
        ans++;
        return;
    }
    for (int c = 0; c < n; c++) {
        int d1 = r + c;
        int d2 = r - c + n - 1;
        if (col[c] || diag1[d1] || diag2[d2]) {
            continue;
        }
        col[c] = diag1[d1] = diag2[d2] = true;
        solve(r + 1);
        col[c] = diag1[d1] = diag2[d2] = false;
    }
}

int main() {
    string line;
    if (!getline(cin, line)) {
        return 0;
    }

    size_t start = 0;
    while (start < line.size() && isspace(static_cast<unsigned char>(line[start]))) {
        start++;
    }
    size_t end = line.size();
    while (end > start && isspace(static_cast<unsigned char>(line[end - 1]))) {
        end--;
    }

    if (start == end) {
        return 0;
    }

    n = stoi(line.substr(start, end - start));

    col.assign(n, false);
    diag1.assign(2 * n - 1, false);
    diag2.assign(2 * n - 1, false);

    solve(0);
    cout << ans << '\n';

    return 0;
}