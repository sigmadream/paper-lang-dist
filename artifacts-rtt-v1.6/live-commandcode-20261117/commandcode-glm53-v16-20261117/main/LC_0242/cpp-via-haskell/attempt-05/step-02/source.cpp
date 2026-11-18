#include <bits/stdc++.h>
using namespace std;

int main(){
    string s, t;
    if(!getline(cin, s)) return 0;
    if(!getline(cin, t)) return 0;
    bool ok = s.size() == t.size();
    if(ok){
        array<int,26> cnt{};
        for(char c : s) cnt[c-'a']++;
        for(char c : t) cnt[c-'a']--;
        for(int x : cnt) if(x != 0) ok = false;
    }
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}