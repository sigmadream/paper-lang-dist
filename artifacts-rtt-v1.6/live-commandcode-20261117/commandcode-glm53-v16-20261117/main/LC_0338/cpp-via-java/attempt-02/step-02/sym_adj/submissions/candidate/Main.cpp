#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; i++) counts[i] = counts[i / 2] + i % 2;
    string out;
    for (int i = 0; i <= n; i++) {
        if (i > 0) out += ' ';
        out += to_string(counts[i]);
    }
    out += '\n';
    fputs(out.c_str(), stdout);
    return 0;
}