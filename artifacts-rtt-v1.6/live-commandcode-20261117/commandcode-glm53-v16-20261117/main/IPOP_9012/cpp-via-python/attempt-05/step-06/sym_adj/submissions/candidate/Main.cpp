#include <bits/stdc++.h>
using namespace std;

int main(){
    int t;
    if(!(cin >> t)) return 0;
    string out;
    for(int i=0;i<t;i++){
        string s;
        if(!(cin >> s)) s = "";
        int bal = 0;
        bool valid = true;
        for(char c : s){
            if(c=='(') bal++;
            else bal--;
            if(bal < 0){ valid = false; break; }
        }
        if(bal != 0) valid = false;
        out += valid ? "YES\n" : "NO\n";
    }
    cout << out;
    return 0;
}