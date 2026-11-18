#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<int> nums;
    int x;
    while (cin >> x) nums.push_back(x);

    if (nums.empty()) return 0;

    int n = nums[0];
    vector<int> scores;
    for (int i = 0; i < n && i + 1 < (int)nums.size(); ++i) {
        scores.push_back(nums[i + 1]);
    }

    if (n == 0) {
        cout << 0 << '\n';
        return 0;
    }

    vector<int> dp(n + 1, 0);

    for (int i = 1; i <= n; ++i) {
        if (i == 1) {
            dp[i] = scores[0];
        } else if (i == 2) {
            dp[i] = scores[0] + scores[1];
        } else {
            dp[i] = max(dp[i - 2], dp[i - 3] + scores[i - 2]) + scores[i - 1];
        }
    }

    cout << dp[n] << '\n';
    return 0;
}