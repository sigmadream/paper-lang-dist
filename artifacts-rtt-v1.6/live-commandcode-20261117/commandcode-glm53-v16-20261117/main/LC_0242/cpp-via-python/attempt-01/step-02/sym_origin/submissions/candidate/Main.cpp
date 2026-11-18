#include <bits/stdc++.h>
using namespace std;

int main(){
    string s, t;
    if(!(cin >> s >> t)) return 0;
    array<int,26> cnt{};
    for(char c : s) cnt[c-'a']++;
    for(char c : t) cnt[c-'a']--;
    bool ok = s.size() == t.size();
    if(ok) for(int x : cnt) if(x != 0) ok = false;
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}