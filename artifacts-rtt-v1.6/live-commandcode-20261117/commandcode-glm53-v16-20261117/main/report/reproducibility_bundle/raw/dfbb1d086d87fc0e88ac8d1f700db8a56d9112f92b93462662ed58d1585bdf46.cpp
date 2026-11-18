#include <bits/stdc++.h>
using namespace std;

int main() {
    string s, t;
    getline(cin, s);
    getline(cin, t);
    array<int, 26> cs{}, ct{};
    for (char c : s) ++cs[c - 'a'];
    for (char c : t) ++ct[c - 'a'];
    cout << (cs == ct ? "1" : "0") << "\n";
    return 0;
}