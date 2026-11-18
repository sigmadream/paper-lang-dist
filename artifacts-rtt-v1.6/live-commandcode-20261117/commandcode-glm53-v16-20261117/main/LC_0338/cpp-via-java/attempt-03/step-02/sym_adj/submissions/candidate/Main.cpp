#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> counts(n + 1);
    string s;
    for (int i = 0; i <= n; i++) {
        if (i > 0) counts[i] = counts[i / 2] + (i % 2);
        if (i > 0) s += ' ';
        s += to_string(counts[i]);
    }
    s += '\n';
    fputs(s.c_str(), stdout);
    return 0;
}