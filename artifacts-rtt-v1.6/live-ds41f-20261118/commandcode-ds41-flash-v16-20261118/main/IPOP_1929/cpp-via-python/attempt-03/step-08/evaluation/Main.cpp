#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, N;
    if (!(cin >> M >> N)) return 0;

    vector<char> is_prime(N + 1, 1);
    if (N >= 0) is_prime[0] = 0;
    if (N >= 1) is_prime[1] = 0;

    for (int i = 2; i * i <= N; ++i) {
        if (is_prime[i]) {
            for (int j = i * i; j <= N; j += i) {
                is_prime[j] = 0;
            }
        }
    }

    for (int x = M; x <= N; ++x) {
        if (is_prime[x]) {
            cout << x << '\n';
        }
    }

    return 0;
}