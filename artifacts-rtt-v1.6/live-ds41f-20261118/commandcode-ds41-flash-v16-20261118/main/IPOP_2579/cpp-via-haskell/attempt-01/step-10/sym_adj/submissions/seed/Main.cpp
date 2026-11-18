#include <bits/stdc++.h>
using namespace std;

static long long solve(int n, const vector<long long>& xs) {
    if (n <= 0) return 0;
    if (xs.empty()) return 0;

    long long s1 = xs[0];
    if (xs.size() == 1) return s1;

    long long s2 = xs[1];

    long long dp3 = 0;
    long long dp2 = s1;
    long long dp1 = s1 + s2;
    long long prevScore = s2;

    for (size_t i = 2; i < xs.size(); ++i) {
        long long score = xs[i];
        long long cur = max(dp2, dp3 + prevScore) + score;
        dp3 = dp2;
        dp2 = dp1;
        dp1 = cur;
        prevScore = score;
    }

    return dp1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<long long> scores;
    scores.reserve(max(0, n));

    for (int i = 0; i < n; ++i) {
        long long x;
        if (!(cin >> x)) break;
        scores.push_back(x);
    }

    cout << solve(n, scores) << '\n';
    return 0;
}