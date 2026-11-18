#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

long long solve(int n, const vector<long long>& xs) {
    if (n <= 0) return 0;
    if (n == 1) {
        return xs.empty() ? 0 : xs[0];
    }
    if (n == 2) {
        if (xs.size() < 2) return 0;
        return xs[0] + xs[1];
    }
    if (xs.size() < 2) return 0;

    long long s1 = xs[0];
    long long s2 = xs[1];
    long long limit = min<long long>(xs.size(), n);

    long long p1 = s1 + s2;
    long long p2 = s1;
    long long p3 = 0;
    long long prev = s2;

    for (long long i = 2; i < limit; ++i) {
        long long cur = xs[i];
        long long nxt = max(p2, p3 + prev) + cur;
        long long old_p1 = p1;
        long long old_p2 = p2;
        p1 = nxt;
        p2 = old_p1;
        p3 = old_p2;
        prev = cur;
    }

    return p1;
}

int main() {
    vector<long long> nums;
    long long x;
    while (cin >> x) nums.push_back(x);

    if (nums.empty()) return 0;

    int n = static_cast<int>(nums[0]);
    vector<long long> xs(nums.begin() + 1, nums.end());

    cout << solve(n, xs) << '\n';
    return 0;
}