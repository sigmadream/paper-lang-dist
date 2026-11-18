#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    cin >> s >> t;
    array<int, 26> cnt{};
    for (char c : s) cnt[c - 'a']++;
    for (char c : t) cnt[c - 'a']--;
    bool ok = true;
    for (int i = 0; i < 26; i++) if (cnt[i] != 0) ok = false;
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}