#include <bits/stdc++.h>
using namespace std;

int main() {
    string s, t;
    if (!(cin >> s)) return 0;
    if (!(cin >> t)) return 0;
    if (s.size() != t.size()) { cout << 0 << "\n"; return 0; }
    int cnt[26] = {0};
    for (char c : s) cnt[c - 'a']++;
    for (char c : t) cnt[c - 'a']--;
    for (int i = 0; i < 26; ++i)
        if (cnt[i] != 0) { cout << 0 << "\n"; return 0; }
    cout << 1 << "\n";
    return 0;
}