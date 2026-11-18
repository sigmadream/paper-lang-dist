#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    long long cur, best;
    bool first = true;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        if (first) { cur = x; best = x; first = false; }
        else {
            cur = max(x, cur + x);
            best = max(best, cur);
        }
    }
    if (!first) cout << best << "\n";
    return 0;
}