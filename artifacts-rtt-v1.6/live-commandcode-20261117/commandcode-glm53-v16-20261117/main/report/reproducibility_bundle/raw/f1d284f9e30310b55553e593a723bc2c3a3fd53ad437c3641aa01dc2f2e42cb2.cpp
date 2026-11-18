#include <bits/stdc++.h>
using namespace std;

int main(){
    string line;
    if(!getline(cin, line)) { cout << 0 << "\n"; return 0; }
    long long n = 0;
    size_t i = 0;
    while(i < line.size() && line[i]==' ') i++;
    bool any=false;
    for(; i<line.size(); ++i){
        if(line[i]>='0' && line[i]<='9'){ n = n*10 + (line[i]-'0'); any=true; }
        else break;
    }
    if(!any) n = 0;
    vector<int> cnts(n+1, 0);
    for(long long k=1;k<=n;++k) cnts[k] = cnts[k/2] + (int)(k%2);
    string out;
    for(long long k=0;k<=n;++k){
        if(k) out += ' ';
        out += to_string(cnts[k]);
    }
    out += '\n';
    cout << out;
    return 0;
}