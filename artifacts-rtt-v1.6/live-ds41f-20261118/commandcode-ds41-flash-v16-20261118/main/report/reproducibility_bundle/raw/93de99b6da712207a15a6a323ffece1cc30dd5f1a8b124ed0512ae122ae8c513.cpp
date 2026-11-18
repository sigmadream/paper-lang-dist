#include <bits/stdc++.h>
using namespace std;

bool parseLL(const string& s, long long& out) {
    if (s.empty()) return false;
    try {
        size_t idx = 0;
        long long v = stoll(s, &idx, 10);
        if (idx != s.size()) return false;
        out = v;
        return true;
    } catch (...) {
        return false;
    }
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

    const long long intMax = 2147483647LL;
    long long k;
    if (n <= 0) k = 0;
    else if (n > intMax) k = intMax;
    else k = n;

    vector<long long> nums;
    size_t i = 1;
    while (i < toks.size() && (long long)nums.size() < k) {
        long long v;
        if (!parseLL(toks[i], v)) break;
        nums.push_back(v);
        ++i;
    }

    if (nums.empty()) {
        cout << 0 << "\n";
        return 0;
    }

    long long cur = nums[0];
    long long best = nums[0];
    for (size_t j = 1; j < nums.size(); ++j) {
        long long v = nums[j];
        cur = max(v, cur + v);
        best = max(best, cur);
    }

    cout << best << "\n";
    return 0;
}