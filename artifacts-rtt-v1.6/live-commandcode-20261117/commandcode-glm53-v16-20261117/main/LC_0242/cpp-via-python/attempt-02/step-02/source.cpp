#include <bits/stdc++.h>
using namespace std;

int main() {
    string s, t;
    cin >> s >> t;
    int cnt[26] = {0};
    for (char c : s) cnt[c - 'a']++;
    for (char c : t) cnt[c - 'a']--;
    bool ok = true;
    for (int i = 0; i < 26; i++) if (cnt[i] != 0) ok = false;
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}