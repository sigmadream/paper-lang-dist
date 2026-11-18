#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    if (!(cin >> s)) return 0;

    string r = s;
    reverse(r.begin(), r.end());
    cout << (s == r ? 1 : 0) << '\n';

    return 0;
}