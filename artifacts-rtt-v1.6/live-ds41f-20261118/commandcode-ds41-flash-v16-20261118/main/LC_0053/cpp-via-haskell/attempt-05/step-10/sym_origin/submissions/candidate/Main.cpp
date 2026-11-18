#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) return 0;
    if (n <= 0) return 0;

    vector<long long> nums;
    nums.reserve(static_cast<size_t>(n));

    for (long long i = 0; i < n; ++i) {
        long long v;
        if (cin >> v) nums.push_back(v);
        else break;
    }

    if (nums.empty()) return 0;

    long long best = nums[0];
    long long cur = nums[0];

    for (size_t i = 1; i < nums.size(); ++i) {
        long long v = nums[i];
        cur = max(v, cur + v);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}