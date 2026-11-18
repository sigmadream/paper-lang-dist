#include <bits/stdc++.h>
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
    for (int i = 1; i < (int)nums.size() && (int)scores.size() < n; ++i) {
        scores.push_back(nums[i]);
    }

    if (n <= 0) {
        cout << 0 << '\n';
        return 0;
    }

    if (n == 1) {
        cout << scores[0] << '\n';
        return 0;
    }

    if (n == 2) {
        cout << scores[0] + scores[1] << '\n';
        return 0;
    }

    int s0 = scores[0];
    int s1 = scores[1];

    int d3 = 0;
    int d2 = s0;
    int d1 = s0 + s1;
    int prev = s1;

    for (int idx = 2; idx < n; ++idx) {
        int s = scores[idx];
        int dCur = max(d2, d3 + prev) + s;

        d3 = d2;
        d2 = d1;
        d1 = dCur;
        prev = s;
    }

    cout << d1 << '\n';
    return 0;
}