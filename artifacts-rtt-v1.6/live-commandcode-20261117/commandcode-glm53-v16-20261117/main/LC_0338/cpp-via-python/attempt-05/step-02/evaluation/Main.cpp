#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n;
    cin >> n;
    vector<int> counts(n + 1, 0);
    for (long long i = 1; i <= n; ++i)
        counts[i] = counts[i / 2] + (int)(i % 2);
    for (size_t i = 0; i < counts.size(); ++i) {
        if (i) cout << ' ';
        cout << counts[i];
    }
    cout << '\n';
    return 0;
}