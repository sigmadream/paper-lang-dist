#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    vector<long long> res;
    int zeros = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] != 0) res.push_back(a[i]);
        else zeros++;
    }
    for (int i = 0; i < zeros; i++) res.push_back(0);
    for (size_t i = 0; i < res.size(); i++) {
        if (i) cout << ' ';
        cout << res[i];
    }
    cout << '\n';
    return 0;
}