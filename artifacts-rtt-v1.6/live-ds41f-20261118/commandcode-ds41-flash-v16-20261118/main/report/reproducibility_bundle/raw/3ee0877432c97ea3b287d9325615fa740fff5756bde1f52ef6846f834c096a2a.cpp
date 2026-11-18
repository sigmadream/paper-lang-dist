#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<long long> nums;
    long long x;
    while (cin >> x) nums.push_back(x);

    if (nums.empty()) return 0;

    long long n = nums[0];
    if (n <= 0) return 0;

    if (nums.size() < 2) return 0;

    long long cur = nums[1];
    long long best = cur;

    for (long long i = 2; i <= n && i < (long long)nums.size(); ++i) {
        cur = max(nums[i], cur + nums[i]);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}