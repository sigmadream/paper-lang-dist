#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    getline(cin, s);
    getline(cin, t);

    s.erase(remove(s.begin(), s.end(), '\r'), s.end());
    t.erase(remove(t.begin(), t.end(), '\r'), t.end());

    sort(s.begin(), s.end());
    sort(t.begin(), t.end());

    cout << (s == t ? 1 : 0) << '\n';
    return 0;
}