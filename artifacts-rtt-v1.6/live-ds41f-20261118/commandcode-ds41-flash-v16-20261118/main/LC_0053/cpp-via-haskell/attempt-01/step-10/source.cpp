#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<long long> tokens;
    long long x;
    while (cin >> x) tokens.push_back(x);

    if (tokens.empty()) return 0;

    long long n = tokens[0];
    long long cnt = max(0LL, n);

    vector<long long> vals;
    for (size_t i = 1; i < tokens.size() && (long long)vals.size() < cnt; ++i) {
        vals.push_back(tokens[i]);
    }

    if (vals.empty()) {
        cout << 0 << "\n";
        return 0;
    }

    long long cur = vals[0];
    long long best = vals[0];

    for (size_t i = 1; i < vals.size(); ++i) {
        cur = max(vals[i], cur + vals[i]);
        best = max(best, cur);
    }

    cout << best << "\n";
    return 0;
}