#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) return 0;
    if (n < 0) n = 0;

    vector<int> counts(static_cast<size_t>(n + 1), 0);
    for (long long i = 1; i <= n; ++i) {
        counts[static_cast<size_t>(i)] =
            counts[static_cast<size_t>(i / 2)] + static_cast<int>(i % 2);
    }

    for (long long i = 0; i <= n; ++i) {
        if (i) cout << ' ';
        cout << counts[static_cast<size_t>(i)];
    }
    cout << '\n';

    return 0;
}