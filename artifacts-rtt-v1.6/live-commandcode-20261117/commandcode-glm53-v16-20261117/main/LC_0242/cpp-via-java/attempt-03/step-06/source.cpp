#include <bits/stdc++.h>
using namespace std;
int main(){
    string s, t;
    getline(cin, s);
    getline(cin, t);
    // trim
    auto trim=[](string& x){
        size_t a=x.find_first_not_of(" \t\r\n");
        size_t b=x.find_last_not_of(" \t\r\n");
        if(a==string::npos) x.clear(); else x=x.substr(a,b-a+1);
    };
    trim(s); trim(t);
    int counts[26]={0};
    for(char c: s) counts[c-'a']++;
    for(char c: t) counts[c-'a']--;
    bool ok=true;
    for(int x: counts) if(x!=0){ok=false;break;}
    cout<<(ok?1:0)<<endl;
    return 0;
}