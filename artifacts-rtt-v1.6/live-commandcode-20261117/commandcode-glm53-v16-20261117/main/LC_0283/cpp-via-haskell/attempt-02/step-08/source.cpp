#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    vector<long long> nonZeros, zeros;
    for (long long x : a) {
        if (x == 0) zeros.push_back(x);
        else nonZeros.push_back(x);
    }
    for (size_t i = 0; i < nonZeros.size(); i++)
        cout << (i ? " " : "") << nonZeros[i];
    for (size_t i = 0; i < zeros.size(); i++)
        cout << " " << zeros[i];
    cout << "\n";
    return 0;
}