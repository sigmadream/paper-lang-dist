#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    if (N <= 0) return 0;

    long long first;
    cin >> first;

    long long cur = first;
    long long best = first;

    for (int i = 1; i < N; ++i) {
        long long x;
        cin >> x;
        cur = max(x, cur + x);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}