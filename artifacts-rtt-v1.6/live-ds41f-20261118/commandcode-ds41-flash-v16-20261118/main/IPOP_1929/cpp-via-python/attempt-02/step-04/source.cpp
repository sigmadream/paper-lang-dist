#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, N;
    if (!(cin >> M >> N)) return 0;

    vector<char> isPrime(N + 1, true);

    if (N >= 0) isPrime[0] = false;
    if (N >= 1) isPrime[1] = false;

    for (int i = 2; 1LL * i * i <= N; ++i) {
        if (isPrime[i]) {
            for (long long j = 1LL * i * i; j <= N; j += i) {
                isPrime[(size_t)j] = false;
            }
        }
    }

    string output;
    for (int i = M; i <= N; ++i) {
        if (isPrime[i]) {
            output += to_string(i);
            output += '\n';
        }
    }

    cout << output;
    return 0;
}