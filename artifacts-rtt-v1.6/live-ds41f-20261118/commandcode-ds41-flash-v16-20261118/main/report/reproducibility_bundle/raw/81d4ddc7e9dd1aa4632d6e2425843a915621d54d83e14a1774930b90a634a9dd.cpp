#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    if (cin >> s >> t) {
        sort(s.begin(), s.end());
        sort(t.begin(), t.end());
        cout << (s == t ? "1" : "0") << '\n';
    }

    return 0;
}