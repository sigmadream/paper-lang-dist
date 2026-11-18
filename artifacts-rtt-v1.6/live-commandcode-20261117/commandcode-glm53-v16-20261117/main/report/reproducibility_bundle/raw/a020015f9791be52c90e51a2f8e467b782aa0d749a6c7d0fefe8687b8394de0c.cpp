#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n);
    for (auto& x : a) cin >> x;
    int idx = 0;
    for (int i = 0; i < n; i++)
        if (a[i] != 0) a[idx++] = a[i];
    for (int i = idx; i < n; i++) a[i] = 0;
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n';
    return 0;
}