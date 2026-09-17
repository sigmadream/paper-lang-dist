// Locally authored C++17 reference for the documented stdin/stdout contract.
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
vector<ll> read_values(int n) {
    vector<ll> a(n); for (ll &x : a) cin >> x; return a;
}
template<class T> void print_values(const vector<T>& a) {
    for (size_t i=0; i<a.size(); ++i) cout << (i ? " " : "") << a[i];
    cout << "\n";
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,e;cin >> n >> e;vector<vector<int>> adj(n);vector<int> indeg(n,0);
    while(e--) {int a,b;cin >> a >> b;adj[b].push_back(a);++indeg[a];}
    queue<int> q;for(int i=0;i<n;++i) if(!indeg[i]) q.push(i);int count=0;
    while(!q.empty()) {int u=q.front();q.pop();++count;for(int v:adj[u]) if(!--indeg[v]) q.push(v);}
    cout << (count==n) << "\n";
    return 0;
}
