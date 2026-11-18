#include <bits/stdc++.h>
using namespace std;

long long solve(int n, const vector<long long>& xs) {
    if (n <= 0) return 0;
    if (n == 1) {
        if (!xs.empty()) return xs[0];
        return 0;
    }
    if (n == 2) {
        if (xs.size() >= 2) return xs[0] + xs[1];
        return 0;
    }

    if (xs.size() < 2) return 0;

    long long s1 = xs[0];
    long long s2 = xs[1];

    long long p1 = s1 + s2;
    long long p2 = s1;
    long long p3 = 0;
    long long prev = s2;

    int limit = min((int)xs.size(), n);
    for (int i = 2; i < limit; ++i) {
        long long cur = xs[i];
        long long nxt = max(p2, p3 + prev) + cur;

        p3 = p2;
        p2 = p1;
        p1 = nxt;
        prev = cur;
    }

    return p1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<long long> nums;
    long long x;
    while (cin >> x) nums.push_back(x);

    if (nums.empty()) return 0;

    int n = static_cast<int>(nums[0]);
    vector<long long> xs(nums.begin() + 1, nums.end());

    cout << solve(n, xs) << '\n';

    return 0;
}