#include <bits/stdc++.h>
using namespace std;

int main(){
    int t;
    if(!(cin >> t)) return 0;
    string s;
    for(int i=0;i<t;i++){
        cin >> s;
        bool valid = true;
        int bal = 0;
        for(char c : s){
            if(c=='(') bal++;
            else bal--;
            if(bal < 0){ valid = false; break; }
        }
        if(bal != 0) valid = false;
        cout << (valid ? "YES" : "NO") << "\n";
    }
    return 0;
}