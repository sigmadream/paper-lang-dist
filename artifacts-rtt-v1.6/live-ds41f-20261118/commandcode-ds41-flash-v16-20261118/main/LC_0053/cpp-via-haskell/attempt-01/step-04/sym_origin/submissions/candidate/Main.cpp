#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) return 0;

    if (n == 0) {
        cout << 0 << '\n';
        return 0;
    }

    long long cur = 0, best = 0;
    bool first = true;

    for (long long i = 0; i < n; ++i) {
        long long x;
        cin >> x;

        if (first) {
            cur = best = x;
            first = false;
        } else {
            cur = max(x, cur + x);
            best = max(best, cur);
        }
    }

    cout << best << '\n';
    return 0;
}