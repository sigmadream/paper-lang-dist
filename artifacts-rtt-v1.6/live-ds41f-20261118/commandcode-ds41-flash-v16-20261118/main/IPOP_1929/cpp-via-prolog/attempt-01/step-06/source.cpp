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

    for (int i = 2; 1LL * i * i <= N; ++i) {
        if (isPrime[i]) {
            for (long long j = 1LL * i * i; j <= N; j += i) {
                isPrime[(int)j] = false;
            }
        }
    }

    int start = max(M, 2);
    for (int i = start; i <= N; ++i) {
        if (isPrime[i]) {
            cout << i << '\n';
        }
    }

    return 0;
}