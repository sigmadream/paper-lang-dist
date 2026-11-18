#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> xs(n);
    for (int i = 0; i < n; i++) cin >> xs[i];
    vector<long long> out;
    int zeros = 0;
    for (int i = 0; i < n; i++) {
        if (xs[i] != 0) out.push_back(xs[i]);
        else zeros++;
    }
    for (int i = 0; i < zeros; i++) out.push_back(0);
    for (size_t i = 0; i < out.size(); i++) {
        if (i) cout << ' ';
        cout << out[i];
    }
    cout << '\n';
    return 0;
}