#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) {
        return 0;
    }

    long long val;
    if (!(cin >> val)) {
        return 0;
    }

    long long cur = val;
    long long best = val;
    for (int i = 1; i < n; ++i) {
        if (!(cin >> val)) {
            break;
        }
        cur = max(val, cur + val);
        best = max(best, cur);
    }

    cout << best << "\n";
    return 0;
}
