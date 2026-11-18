#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<long long> nums;
    long long x;
    while (cin >> x) nums.push_back(x);

    if (nums.empty()) {
        cout << '\n';
        return 0;
    }

    long long N = nums[0];
    vector<long long> values;
    for (long long i = 1; i < (long long)nums.size() && (long long)values.size() < N; ++i) {
        values.push_back(nums[i]);
    }

    vector<long long> result;
    result.reserve(values.size());

    for (long long v : values) {
        if (v != 0) result.push_back(v);
    }
    for (long long v : values) {
        if (v == 0) result.push_back(v);
    }

    for (size_t i = 0; i < result.size(); ++i) {
        if (i) cout << ' ';
        cout << result[i];
    }
    cout << '\n';

    return 0;
}