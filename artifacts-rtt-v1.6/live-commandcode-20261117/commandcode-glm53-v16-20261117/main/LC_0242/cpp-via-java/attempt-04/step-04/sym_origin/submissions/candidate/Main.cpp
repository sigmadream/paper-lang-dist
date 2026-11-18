#include <bits/stdc++.h>
using namespace std;

int main(){
    string s, t;
    if(!getline(cin, s)) s = "";
    if(!getline(cin, t)) t = "";
    int counts[26] = {0};
    for(char c : s) counts[c - 'a']++;
    for(char c : t) counts[c - 'a']--;
    bool ok = true;
    for(int x : counts) if(x != 0){ ok = false; break; }
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}