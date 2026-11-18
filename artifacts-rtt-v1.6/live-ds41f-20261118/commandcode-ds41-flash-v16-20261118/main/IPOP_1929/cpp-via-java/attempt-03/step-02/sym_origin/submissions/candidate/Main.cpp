#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m, n;
    cin >> m >> n;

    vector<bool> isPrime(n + 1, false);
    for (int i = 2; i <= n; i++) isPrime[i] = true;

    for (int i = 2; (long long)i * i <= n; i++) {
        if (isPrime[i]) {
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }

    string out;
    for (int i = m; i <= n; i++) {
        if (isPrime[i]) {
            out += to_string(i);
            out += '\n';
        }
    }

    cout << out;
    return 0;
}