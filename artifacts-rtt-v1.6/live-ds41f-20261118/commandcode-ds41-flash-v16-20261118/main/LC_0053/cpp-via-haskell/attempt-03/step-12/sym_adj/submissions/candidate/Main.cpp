#include <bits/stdc++.h>
using namespace std;

long long solve(const vector<long long>& v) {
    if (v.empty()) return 0;
    long long cur = v[0];
    long long best = v[0];
    for (size_t i = 1; i < v.size(); ++i) {
        long long y = v[i];
        cur = max(y, cur + y);
        best = max(best, cur);
    }
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<long long> nums;
    long long x;
    while (cin >> x) nums.push_back(x);

    if (nums.empty()) return 0;

    long long n = nums[0];
    if (n <= 0) {
        cout << 0 << '\n';
        return 0;
    }

    vector<long long> rest;
    size_t takeCount = static_cast<size_t>(n);
    size_t available = nums.size() - 1;
    size_t m = min(takeCount, available);
    rest.reserve(m);
    for (size_t i = 0; i < m; ++i) {
        rest.push_back(nums[i + 1]);
    }

    cout << solve(rest) << '\n';
    return 0;
}