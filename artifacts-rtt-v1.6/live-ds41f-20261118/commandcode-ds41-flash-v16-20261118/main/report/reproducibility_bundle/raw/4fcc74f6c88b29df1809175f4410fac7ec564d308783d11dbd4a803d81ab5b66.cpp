#include <iostream>
#include <vector>
#include <string>
#include <climits>
#include <algorithm>

using namespace std;

bool parseLL(const string& s, long long& out) {
    if (s.empty()) return false;
    size_t i = 0;
    bool neg = false;
    if (s[i] == '+' || s[i] == '-') {
        neg = (s[i] == '-');
        ++i;
        if (i == s.size()) return false;
    }
    long long v = 0;
    for (; i < s.size(); ++i) {
        if (!isdigit((unsigned char)s[i])) return false;
        int d = s[i] - '0';
        if (v > (LLONG_MAX - d) / 10) return false;
        v = v * 10 + d;
    }
    out = neg ? -v : v;
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> toks;
    string t;
    while (cin >> t) toks.push_back(t);

    if (toks.empty()) return 0;

    long long n;
    if (!parseLL(toks[0], n)) return 0;

    long long k;
    if (n <= 0) k = 0;
    else if (n > (long long)INT_MAX) k = INT_MAX;
    else k = n;

    vector<long long> nums;
    for (size_t i = 1; i < toks.size() && (long long)nums.size() < k; ++i) {
        long long v;
        if (!parseLL(toks[i], v)) break;
        nums.push_back(v);
    }

    if (nums.empty()) {
        cout << 0 << '\n';
        return 0;
    }

    long long cur = nums[0];
    long long best = nums[0];
    for (size_t i = 1; i < nums.size(); ++i) {
        cur = max(nums[i], cur + nums[i]);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}