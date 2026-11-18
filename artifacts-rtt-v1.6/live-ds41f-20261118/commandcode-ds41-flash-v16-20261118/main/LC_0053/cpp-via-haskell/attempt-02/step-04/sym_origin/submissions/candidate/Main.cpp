#include <bits/stdc++.h>
using namespace std;

static bool parseInteger(const string& s, long long& out) {
    if (s.empty()) return false;
    try {
        size_t pos = 0;
        long long v = stoll(s, &pos, 10);
        if (pos != s.size()) return false;
        out = v;
        return true;
    } catch (...) {
        return false;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> tokens;
    string token;
    while (cin >> token) tokens.push_back(token);

    if (tokens.empty()) return 0;

    long long n;
    if (!parseInteger(tokens[0], n)) return 0;

    int k;
    if (n <= 0) k = 0;
    else if (n > INT_MAX) k = INT_MAX;
    else k = static_cast<int>(n);

    vector<long long> nums;
    nums.reserve(min<int>(k, max<int>(0, static_cast<int>(tokens.size() - 1))));

    for (size_t i = 1; i < tokens.size() && static_cast<int>(nums.size()) < k; ++i) {
        long long x;
        if (!parseInteger(tokens[i], x)) break;
        nums.push_back(x);
    }

    if (nums.empty()) {
        cout << "0\n";
        return 0;
    }

    long long cur = nums[0];
    long long best = nums[0];

    for (size_t i = 1; i < nums.size(); ++i) {
        long long v = nums[i];
        cur = max(v, cur + v);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}