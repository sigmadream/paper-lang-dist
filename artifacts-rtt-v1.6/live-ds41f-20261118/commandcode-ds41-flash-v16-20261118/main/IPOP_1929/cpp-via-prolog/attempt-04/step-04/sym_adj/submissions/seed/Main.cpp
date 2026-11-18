#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, N;
    if (!(cin >> M >> N)) return 0;

    vector<char> isPrime(N + 1, 1);
    if (N >= 0) isPrime[0] = 0;
    if (N >= 1) isPrime[1] = 0;

    for (int p = 2; 1LL * p * p <= N; ++p) {
        if (!isPrime[p]) continue;
        for (long long j = 1LL * p * p; j <= N; j += p) {
            isPrime[(int)j] = 0;
        }
    }

    for (int i = M; i <= N; ++i) {
        if (isPrime[i]) {
            cout << i << '\n';
        }
    }

    return 0;
}