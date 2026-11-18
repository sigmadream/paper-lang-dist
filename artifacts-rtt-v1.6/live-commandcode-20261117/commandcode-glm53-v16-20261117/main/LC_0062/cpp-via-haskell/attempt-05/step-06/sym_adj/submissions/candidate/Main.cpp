#include <bits/stdc++.h>
using namespace std;

int main() {
    long long m, n;
    if (cin >> m >> n) {
        vector<long long> row(n, 1);
        for (long long i = 2; i <= m; ++i) {
            for (long long j = 1; j < n; ++j) row[j] += row[j - 1];
        }
        cout << row[n - 1] << "\n";
    }
    return 0;
}