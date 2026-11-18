#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> nonZero, zeros;
    for (int i = 0; i < n; ++i) {
        int x;
        if (!(cin >> x)) break;
        if (x != 0) nonZero.push_back(x);
        else zeros.push_back(0);
    }

    nonZero.insert(nonZero.end(), zeros.begin(), zeros.end());

    for (size_t i = 0; i < nonZero.size(); ++i) {
        if (i) cout << ' ';
        cout << nonZero[i];
    }
    cout << '\n';

    return 0;
}