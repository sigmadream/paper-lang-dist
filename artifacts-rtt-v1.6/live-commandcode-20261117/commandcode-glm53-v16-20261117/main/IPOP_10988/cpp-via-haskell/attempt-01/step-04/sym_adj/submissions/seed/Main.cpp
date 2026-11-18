#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    if (!(cin >> s)) return 0;
    string t(s.rbegin(), s.rend());
    cout << (s == t ? "1" : "0") << "\n";
    return 0;
}