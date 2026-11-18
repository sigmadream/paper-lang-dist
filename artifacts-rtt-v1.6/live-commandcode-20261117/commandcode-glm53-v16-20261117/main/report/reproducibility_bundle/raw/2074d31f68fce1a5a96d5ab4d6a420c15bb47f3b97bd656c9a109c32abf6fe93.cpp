#include <bits/stdc++.h>
using namespace std;

int main() {
    int m, n;
    if (scanf("%d %d", &m, &n) != 2) return 0;

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

    string out;
    char buf[16];
    for (int i = m; i <= n; i++) {
        if (!isComposite[i]) {
            int len = snprintf(buf, sizeof(buf), "%d\n", i);
            out.append(buf, len);
        }
    }
    fputs(out.c_str(), stdout);
    return 0;
}