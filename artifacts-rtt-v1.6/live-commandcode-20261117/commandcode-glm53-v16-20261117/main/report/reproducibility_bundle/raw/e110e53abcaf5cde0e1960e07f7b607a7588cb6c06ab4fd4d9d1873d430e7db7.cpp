#include <bits/stdc++.h>
using namespace std;
int main(){
    string line;
    if(!getline(cin, line)) return 0;
    int start=0, end=line.size();
    while(end>start && (line[end-1]=='\n'||line[end-1]=='\r'||line[end-1]==' '||line[end-1]=='\t')) end--;
    while(start<end && (line[start]==' '||line[start]=='\t')) start++;
    string s=line.substr(start, end-start);
    bool valid=true;
    for(int i=0;i<(int)s.size()/2;i++){
        if(s[i]!=s[s.size()-1-i]){valid=false;break;}
    }
    cout<<(valid?1:0)<<endl;
    return 0;
}