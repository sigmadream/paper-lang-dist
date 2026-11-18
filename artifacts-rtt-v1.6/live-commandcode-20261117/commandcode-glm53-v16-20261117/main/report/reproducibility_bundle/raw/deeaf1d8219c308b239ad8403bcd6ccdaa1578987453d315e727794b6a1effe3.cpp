#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    cin >> s >> t;
    array<int,26> cnt{};
    for (char c : s) cnt[c-'a']++;
    for (char c : t) cnt[c-'a']--;
    bool ok = all_of(cnt.begin(), cnt.end(), [](int x){ return x == 0; });
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}