#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> a(n);
    for (int &x : a) cin >> x;

    int j = 0;
    for (int i = 0; i < n; ++i) {
        if (a[i] != 0) {
            a[j++] = a[i];
        }
    }
    while (j < n) {
        a[j++] = 0;
    }

    for (int i = 0; i < n; ++i) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n';

    return 0;
}