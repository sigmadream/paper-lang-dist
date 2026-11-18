#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<int> a(N);
    for (int i = 0; i < N; ++i) cin >> a[i];

    long long cur = a[0];
    long long best = a[0];

    for (int i = 1; i < N; ++i) {
        long long sum = cur + a[i];
        cur = (a[i] > sum ? a[i] : sum);
        if (cur > best) best = cur;
    }

    cout << best << '\n';
    return 0;
}