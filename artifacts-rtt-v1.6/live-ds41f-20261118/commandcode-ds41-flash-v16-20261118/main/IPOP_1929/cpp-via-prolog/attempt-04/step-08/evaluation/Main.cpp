#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, N;
    if (!(cin >> M >> N)) return 0;

    vector<bool> isPrime(N + 1, true);
    if (N >= 0) isPrime[0] = false;
    if (N >= 1) isPrime[1] = false;

    for (int p = 2; (long long)p * p <= N; ++p) {
        if (isPrime[p]) {
            for (long long j = 1LL * p * p; j <= N; j += p) {
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