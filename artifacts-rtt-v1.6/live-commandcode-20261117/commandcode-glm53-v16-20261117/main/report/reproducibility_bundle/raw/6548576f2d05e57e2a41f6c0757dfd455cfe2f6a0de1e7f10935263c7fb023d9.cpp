#include <bits/stdc++.h>
using namespace std;

int main(){
    string s, t;
    if(!getline(cin, s)) return 0;
    if(!getline(cin, t)) return 0;
    sort(s.begin(), s.end());
    sort(t.begin(), t.end());
    cout << (s == t ? 1 : 0) << "\n";
    return 0;
}