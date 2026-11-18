#include <bits/stdc++.h>
using namespace std;

int main() {
    string s, t;
    if (!getline(cin, s)) return 0;
    if (!getline(cin, t)) return 0;
    if (s.size() != t.size()) { cout << 0 << "\n"; return 0; }
    array<int, 26> a{}, b{};
    for (char c : s) a[c - 'a']++;
    for (char c : t) b[c - 'a']++;
    cout << (a == b ? 1 : 0) << "\n";
    return 0;
}