#include <bits/stdc++.h>
using namespace std;

int main() {
    string s, t;
    getline(cin, s);
    getline(cin, t);
    if (s.size() != t.size()) { cout << 0 << "\n"; return 0; }
    array<int, 256> a{}, b{};
    for (char c : s) a[(unsigned char)c]++;
    for (char c : t) b[(unsigned char)c]++;
    cout << (a == b ? 1 : 0) << "\n";
    return 0;
}