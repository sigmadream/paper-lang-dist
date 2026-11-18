#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    int pos = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] != 0) a[pos++] = a[i];
    }
    for (int i = pos; i < n; i++) a[i] = 0;
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n';
    return 0;
}