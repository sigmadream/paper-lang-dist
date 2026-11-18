#include <bits/stdc++.h>
using namespace std;

int n, full;

long long go(int r, int cols, int d1, int d2) {
    if (r == n) return 1;
    int avail = full & ~(cols | d1 | d2);
    long long total = 0;
    while (avail) {
        int b = avail & -avail;
        avail ^= b;
        total += go(r + 1, cols | b, ((d1 | b) << 1) & full, (d2 | b) >> 1);
    }
    return total;
}

int main() {
    cin >> n;
    full = (1 << n) - 1;
    cout << go(0, 0, 0, 0) << '\n';
    return 0;
}