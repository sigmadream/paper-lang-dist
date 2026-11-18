#include <bits/stdc++.h>
using namespace std;
int main(){
    string s,t;
    getline(cin,s);
    getline(cin,t);
    auto trim=[](string& str){
        size_t a=str.find_first_not_of(" \t\r\n");
        size_t b=str.find_last_not_of(" \t\r\n");
        if(a==string::npos) str.clear(); else str=str.substr(a,b-a+1);
    };
    trim(s); trim(t);
    int counts[26]={0};
    for(char c:s) counts[c-'a']++;
    for(char c:t) counts[c-'a']--;
    bool ok=true;
    for(int x:counts) if(x!=0){ok=false;break;}
    cout<<(ok?1:0)<<"\n";
    return 0;
}