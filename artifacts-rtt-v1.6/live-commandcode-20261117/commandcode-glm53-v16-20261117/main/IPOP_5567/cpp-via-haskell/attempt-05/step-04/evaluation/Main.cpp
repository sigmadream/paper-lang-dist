#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    if(!(cin>>n)) return 0;
    cin>>m;
    vector<vector<int>> adj(n+1);
    vector<pair<int,int>> edges;
    for(int i=0;i<m;i++){
        int a,b; cin>>a>>b;
        edges.push_back({a,b});
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    set<int> d1;
    for(auto&e:edges){
        if(e.first==1) d1.insert(e.second);
        if(e.second==1) d1.insert(e.first);
    }
    d1.erase(1);
    set<int> d2;
    for(int v:d1) for(int w:adj[v]) d2.insert(w);
    d2.erase(1);
    set<int> ans;
    set_union(d1.begin(),d1.end(),d2.begin(),d2.end(),inserter(ans,ans.begin()));
    cout<<ans.size()<<"\n";
    return 0;
}