#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a;
    long long x;
    for (int i = 0; i < n && (cin >> x); ++i) a.push_back(x);
    stable_partition(a.begin(), a.end(), [](long long v){ return v != 0; });
    for (size_t i = 0; i < a.size(); ++i) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n';
    return 0;
}