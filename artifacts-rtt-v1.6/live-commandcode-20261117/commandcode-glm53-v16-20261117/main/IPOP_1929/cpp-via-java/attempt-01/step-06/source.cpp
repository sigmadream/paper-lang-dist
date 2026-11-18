#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m, n;
    cin >> m >> n;

    vector<bool> isComposite(n + 1, false);
    if (n >= 0) isComposite[0] = true;
    if (n >= 1) isComposite[1] = true;

    for (long long i = 2; i * i <= n; i++) {
        if (!isComposite[(int)i]) {
            for (long long j = i * i; j <= n; j += i) {
                isComposite[(int)j] = true;
            }
        }
    }

    for (int i = m; i <= n; i++) {
        if (!isComposite[i]) {
            cout << i << '\n';
        }
    }
    return 0;
}