#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long N;
    if (!(cin >> N)) return 0;

    long long best = 0;
    long long cur = 0;
    bool first = true;

    for (long long i = 0; i < N; ++i) {
        long long x;
        cin >> x;

        if (first) {
            cur = x;
            best = x;
            first = false;
        } else {
            cur = max(x, cur + x);
            best = max(best, cur);
        }
    }

    cout << best << '\n';
    return 0;
}