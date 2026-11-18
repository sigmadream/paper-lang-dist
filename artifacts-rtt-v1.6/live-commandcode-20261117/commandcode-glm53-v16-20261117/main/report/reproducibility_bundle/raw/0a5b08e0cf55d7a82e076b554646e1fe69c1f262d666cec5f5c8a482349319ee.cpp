#include <bits/stdc++.h>
using namespace std;

int n;
int cols[15], d1[30], d2[30];

int solve(int r) {
    if (r == n) return 1;
    int total = 0;
    for (int c = 0; c < n; ++c) {
        if (cols[c] || d1[r+c] || d2[r-c+n-1]) continue;
        cols[c] = d1[r+c] = d2[r-c+n-1] = 1;
        total += solve(r+1);
        cols[c] = d1[r+c] = d2[r-c+n-1] = 0;
    }
    return total;
}

int main() {
    if (!(cin >> n)) return 0;
    cout << solve(0) << "\n";
    return 0;
}