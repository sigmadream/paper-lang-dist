#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long M, N;
    if (!(cin >> M >> N)) return 0;

    vector<long long> row(N, 1);

    for (long long k = 1; k < M; ++k) {
        for (long long i = 1; i < N; ++i) {
            row[i] += row[i - 1];
        }
    }

    cout << row[N - 1] << '\n';
    return 0;
}