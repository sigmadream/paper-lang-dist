#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> nums(n);
    for (int i = 0; i < n; ++i) cin >> nums[i];
    if (nums.empty()) return 0;
    long long best = nums[0], cur = nums[0];
    for (int i = 1; i < n; ++i) {
        cur = max(nums[i], cur + nums[i]);
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}