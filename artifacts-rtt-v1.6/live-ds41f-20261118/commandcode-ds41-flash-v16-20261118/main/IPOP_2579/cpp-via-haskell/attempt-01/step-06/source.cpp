#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int solve(int n, const vector<int>& rest) {
    if (n <= 0) return 0;

    if (n == 1) {
        return rest.empty() ? 0 : rest[0];
    }

    if (n == 2) {
        return rest.size() >= 2 ? rest[0] + rest[1] : 0;
    }

    if (rest.size() < 2) return 0;

    int s0 = rest[0];
    int s1 = rest[1];

    long long d3 = 0;
    long long d2 = s0;
    long long d1 = s0 + s1;
    long long prev = s1;

    for (int i = 2; i < n && i < static_cast<int>(rest.size()); ++i) {
        int s = rest[i];
        long long dCur = max(d2, d3 + prev) + s;

        d3 = d2;
        d2 = d1;
        d1 = dCur;
        prev = s;
    }

    return static_cast<int>(d1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> scores(n);
    for (int i = 0; i < n; ++i) {
        cin >> scores[i];
    }

    cout << solve(n, scores) << '\n';

    return 0;
}