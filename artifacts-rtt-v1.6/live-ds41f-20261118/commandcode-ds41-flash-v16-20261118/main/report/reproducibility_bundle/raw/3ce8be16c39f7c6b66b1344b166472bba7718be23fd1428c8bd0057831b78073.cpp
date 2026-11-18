#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, N;
    if (!(cin >> M >> N)) return 0;

    vector<char> isPrime(N + 1, true);
    isPrime[0] = false;
    if (N >= 1) isPrime[1] = false;

    for (long long p = 2; p * p <= N; ++p) {
        if (isPrime[p]) {
            for (long long j = p * p; j <= N; j += p) {
                isPrime[j] = false;
            }
        }
    }

    for (int i = M; i <= N; ++i) {
        if (isPrime[i]) cout << i << '\n';
    }

    return 0;
}