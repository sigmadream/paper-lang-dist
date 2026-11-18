#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<long long> tokens;
    long long v;
    while (cin >> v) tokens.push_back(v);

    if (tokens.empty()) return 0;

    int n = (int)tokens[0];
    if (n <= 0) return 0;

    int m = min(n, (int)tokens.size() - 1);
    if (m <= 0) return 0;

    long long first = tokens[1];
    long long cur = first;
    long long best = first;

    for (int i = 2; i <= m; ++i) {
        long long y = tokens[i];
        cur = max(y, cur + y);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}