#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    cin >> s >> t;
    array<int, 26> cs{}, ct{};
    for (char c : s) cs[c - 'a']++;
    for (char c : t) ct[c - 'a']++;
    cout << (cs == ct ? 1 : 0) << "\n";
    return 0;
}