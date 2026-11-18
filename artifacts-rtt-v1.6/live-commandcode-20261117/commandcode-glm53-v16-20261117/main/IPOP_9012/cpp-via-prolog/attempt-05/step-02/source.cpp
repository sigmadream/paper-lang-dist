#include <bits/stdc++.h>
using namespace std;

int main(){
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if(!(cin >> T)) return 0;
    string s;
    for(int i=0;i<T;i++){
        if(!(cin >> s)) break;
        long long bal = 0;
        bool neg = false;
        for(char c : s){
            bal += (c=='(') ? 1 : -1;
            if(bal < 0){ neg = true; break; }
        }
        cout << ((bal==0 && !neg) ? "YES" : "NO") << '\n';
    }
    return 0;
}