#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, N;
    if (!(cin >> M >> N)) return 0;

    vector<long long> row(N, 1);

    for (int i = 1; i < M; ++i) {
        for (int j = 1; j < N; ++j) {
            row[j] += row[j - 1];
        }
    }

    cout << row.back() << '\n';
    return 0;
}