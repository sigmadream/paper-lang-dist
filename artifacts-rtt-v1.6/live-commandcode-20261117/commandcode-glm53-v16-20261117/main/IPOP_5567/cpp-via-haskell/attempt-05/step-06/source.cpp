#include <bits/stdc++.h>
using namespace std;
int main(){
    int n, m;
    if(!(cin >> n >> m)) { cout << 0 << "\n"; return 0; }
    vector<vector<int>> adj(n+1);
    for(int i=0;i<m;i++){
        int a,b; cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    set<int> d1;
    for(int v: adj[1]) if(v!=1) d1.insert(v);
    set<int> d2;
    for(int v: d1) for(int w: adj[v]) if(w!=1) d2.insert(w);
    set<int> ans = d1;
    ans.insert(d2.begin(), d2.end());
    cout << ans.size() << "\n";
}