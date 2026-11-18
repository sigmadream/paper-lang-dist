#include <bits/stdc++.h>
using namespace std;

int main(){
    int n;
    if(scanf("%d",&n)!=1) return 0;
    // total moves = 2^n - 1
    vector<pair<int,int>> moves;
    moves.reserve((1u<<n)-1);
    // iterative or recursive; n<=20 so recursion depth fine
    function<void(int,int,int,int)> hanoi=[&](int n,int s,int m,int e){
        if(n==1){ moves.push_back({s,e}); return; }
        hanoi(n-1,s,e,m);
        moves.push_back({s,e});
        hanoi(n-1,m,s,e);
    };
    hanoi(n,1,2,3);
    string out;
    out.reserve(moves.size()*4+16);
    out += to_string(moves.size());
    out += '\n';
    for(auto& p: moves){
        out += char('0'+p.first);
        out += ' ';
        out += char('0'+p.second);
        out += '\n';
    }
    fwrite(out.data(),1,out.size(),stdout);
    return 0;
}