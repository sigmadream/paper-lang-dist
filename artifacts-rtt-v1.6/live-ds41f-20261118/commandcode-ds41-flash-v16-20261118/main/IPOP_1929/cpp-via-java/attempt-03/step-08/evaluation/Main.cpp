#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, N;
    cin >> M >> N;

    vector<bool> isPrime(N + 1, true);
    if (N >= 0) isPrime[0] = false;
    if (N >= 1) isPrime[1] = false;

    for (int i = 2; (long long)i * i <= N; ++i) {
        if (isPrime[i]) {
            for (long long j = (long long)i * i; j <= N; j += i) {
                isPrime[(int)j] = false;
            }
        }
    }

    for (int i = M; i <= N; ++i) {
        if (isPrime[i]) {
            cout << i << '\n';
        }
    }

    return 0;
}