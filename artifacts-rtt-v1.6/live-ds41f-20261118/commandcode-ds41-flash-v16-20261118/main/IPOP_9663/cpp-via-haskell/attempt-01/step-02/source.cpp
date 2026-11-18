#include <bits/stdc++.h>
using namespace std;

static int n;
static int full;

static long long solve(int r, int cols, int d1, int d2) {
    if (r == n) return 1;
    int avail = full & ~(cols | d1 | d2);
    long long acc = 0;
    while (avail) {
        int bit = avail & -avail;
        avail &= avail - 1;
        acc += solve(r + 1, cols | bit, (d1 | bit) << 1, (d2 | bit) >> 1);
    }
    return acc;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    if (!(cin >> n)) return 0;
    full = (1 << n) - 1;
    cout << solve(0, 0, 0, 0) << '\n';
    return 0;
}