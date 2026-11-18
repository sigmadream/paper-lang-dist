#include <bits/stdc++.h>
using namespace std;

int main(){
    string s, t;
    if(!(cin >> s)) return 0;
    if(!(cin >> t)) return 0;
    if(s.size() != t.size()){ cout << 0 << "\n"; return 0; }
    array<int,26> cnt{};
    for(char c : s) cnt[c-'a']++;
    for(char c : t) cnt[c-'a']--;
    bool ok = true;
    for(int x : cnt) if(x != 0) ok = false;
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}