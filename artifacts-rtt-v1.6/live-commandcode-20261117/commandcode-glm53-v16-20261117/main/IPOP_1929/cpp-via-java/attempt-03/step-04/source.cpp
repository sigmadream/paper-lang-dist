#include <bits/stdc++.h>
using namespace std;

int main() {
    int m, n;
    if (scanf("%d %d", &m, &n) != 2) return 0;

    vector<bool> isComposite(n + 1, false);
    if (n >= 0) isComposite[0] = true;
    if (n >= 1) isComposite[1] = true;

    for (long long i = 2; i * i <= n; i++) {
        if (!isComposite[(size_t)i]) {
            for (long long j = i * i; j <= n; j += i) {
                isComposite[(size_t)j] = true;
            }
        }
    }

    string out;
    for (int i = m; i <= n; i++) {
        if (!isComposite[i]) {
            out += to_string(i);
            out += '\n';
        }
    }
    fputs(out.c_str(), stdout);
    return 0;
}