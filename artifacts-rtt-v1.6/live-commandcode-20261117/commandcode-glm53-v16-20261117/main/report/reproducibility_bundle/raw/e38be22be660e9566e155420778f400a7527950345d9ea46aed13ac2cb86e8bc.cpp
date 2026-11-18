#include <bits/stdc++.h>
using namespace std;

int main(){
    string s, t;
    if(!(cin >> s >> t)) return 0;
    array<int,26> counts{};
    for(char c : s) counts[c-'a']++;
    for(char c : t) counts[c-'a']--;
    bool ok = true;
    for(int x : counts) if(x != 0) ok = false;
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}