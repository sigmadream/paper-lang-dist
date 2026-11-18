#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, N;
    if (!(cin >> M >> N)) return 0;

    vector<char> is_prime(N + 1, true);
    if (N >= 0) is_prime[0] = false;
    if (N >= 1) is_prime[1] = false;

    for (long long i = 2; i * i <= N; ++i) {
        if (is_prime[i]) {
            for (long long j = i * i; j <= N; j += i) {
                is_prime[j] = false;
            }
        }
    }

    for (int i = M; i <= N; ++i) {
        if (is_prime[i]) {
            cout << i << '\n';
        }
    }

    return 0;
}