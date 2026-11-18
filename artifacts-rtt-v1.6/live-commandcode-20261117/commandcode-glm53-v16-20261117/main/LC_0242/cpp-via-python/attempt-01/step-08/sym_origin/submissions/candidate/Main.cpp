#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    if (!(cin >> s >> t)) return 0;
    if (s.size() != t.size()) { cout << 0 << "\n"; return 0; }
    array<int,26> cnt{};
    for (char c : s) cnt[c - 'a']++;
    for (char c : t) cnt[c - 'a']--;
    bool ok = all_of(cnt.begin(), cnt.end(), [](int x){ return x == 0; });
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}