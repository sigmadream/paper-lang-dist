"""Locally authored standalone C++17 references, not copies of upstream code."""

HEADER = '''// Locally authored C++17 reference for the documented stdin/stdout contract.
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
vector<ll> read_values(int n) {
    vector<ll> a(n); for (ll &x : a) cin >> x; return a;
}
template<class T> void print_values(const vector<T>& a) {
    for (size_t i=0; i<a.size(); ++i) cout << (i ? " " : "") << a[i];
    cout << "\\n";
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
'''

BODIES = {
1: '''    int n; ll target; cin >> n >> target; auto a=read_values(n);
    unordered_map<ll,int> seen;
    for (int i=0;i<n;++i) {
        auto it=seen.find(target-a[i]);
        if(it!=seen.end()) { cout << it->second << " " << i << "\\n"; return 0; }
        seen[a[i]]=i;
    }
''',
121: '''    int n; cin >> n; auto a=read_values(n); ll low=a[0],best=0;
    for(ll x:a) { best=max(best,x-low); low=min(low,x); }
    cout << best << "\\n";
''',
217: '''    int n; cin >> n; auto a=read_values(n); unordered_set<ll> seen;
    bool duplicate=false;
    for(ll x:a) if(!seen.insert(x).second) duplicate=true;
    cout << duplicate << "\\n";
''',
53: '''    int n; cin >> n; auto a=read_values(n); ll cur=a[0],best=a[0];
    for(int i=1;i<n;++i) {cur=max(a[i],cur+a[i]);best=max(best,cur);}
    cout << best << "\\n";
''',
704: '''    int n; ll target; cin >> n >> target; auto a=read_values(n);
    int lo=0,hi=n;
    while(lo<hi) {int mid=lo+(hi-lo)/2; if(a[mid]<target) lo=mid+1; else hi=mid;}
    cout << (lo<n && a[lo]==target ? lo : -1) << "\\n";
''',
35: '''    int n; ll target; cin >> n >> target; auto a=read_values(n);
    int lo=0,hi=n;
    while(lo<hi) {int mid=lo+(hi-lo)/2; if(a[mid]<target) lo=mid+1; else hi=mid;}
    cout << lo << "\\n";
''',
283: '''    int n; cin >> n; auto a=read_values(n); int write=0;
    for(int read=0;read<n;++read) if(a[read]) swap(a[write++],a[read]);
    print_values(a);
''',
242: '''    string s,t; cin >> s >> t; array<int,26> counts{};
    for(char c:s) ++counts[c-'a']; for(char c:t) --counts[c-'a'];
    cout << all_of(counts.begin(),counts.end(),[](int x){return x==0;}) << "\\n";
''',
387: '''    string s; cin >> s; array<int,26> counts{}; for(char c:s) ++counts[c-'a'];
    int answer=-1; for(int i=0;i<(int)s.size();++i) if(counts[s[i]-'a']==1) {answer=i;break;}
    cout << answer << "\\n";
''',
3: '''    string s; getline(cin,s); if(!s.empty() && s.back()=='\\r') s.pop_back();
    array<int,256> last; last.fill(-1); int start=0,best=0;
    for(int i=0;i<(int)s.size();++i) {
        unsigned char c=s[i]; start=max(start,last[c]+1);best=max(best,i-start+1);last[c]=i;
    }
    cout << best << "\\n";
''',
139: '''    string s; int k; cin >> s >> k; vector<string> words(k); for(auto &w:words) cin >> w;
    vector<bool> dp(s.size()+1,false);dp[0]=true;
    for(size_t i=1;i<=s.size();++i) for(const auto &w:words)
        if(w.size()<=i && dp[i-w.size()] && s.compare(i-w.size(),w.size(),w)==0) {dp[i]=true;break;}
    cout << dp.back() << "\\n";
''',
518: '''    int amount,k; cin >> amount >> k; auto coins=read_values(k);
    vector<unsigned long long> dp(amount+1,0);dp[0]=1;
    for(ll coin:coins) for(int x=(int)coin;x<=amount;++x)
        dp[x]=min(2147483648ULL,dp[x]+dp[x-coin]);
    cout << dp[amount] << "\\n";
''',
62: '''    int m,n; cin >> m >> n; vector<ll> dp(n,1);
    for(int i=1;i<m;++i) for(int j=1;j<n;++j) dp[j]+=dp[j-1];
    cout << dp.back() << "\\n";
''',
63: '''    int m,n; cin >> m >> n; vector<ll> dp(n,0);dp[0]=1;
    for(int i=0;i<m;++i) for(int j=0;j<n;++j) {
        int blocked;cin >> blocked;
        if(blocked) dp[j]=0;else if(j) dp[j]=min(2000000001LL,dp[j]+dp[j-1]);
    }
    cout << dp.back() << "\\n";
''',
64: '''    int m,n; cin >> m >> n; vector<ll> dp(n,LLONG_MAX/4);
    for(int i=0;i<m;++i) for(int j=0;j<n;++j) {
        ll value;cin >> value;
        if(!i && !j) dp[j]=value;
        else dp[j]=value+min(dp[j],j ? dp[j-1] : LLONG_MAX/4);
    }
    cout << dp.back() << "\\n";
''',
739: '''    int n; cin >> n;auto a=read_values(n);vector<int> out(n,0),pending;
    for(int i=0;i<n;++i) {
        while(!pending.empty() && a[pending.back()]<a[i]) {
            int j=pending.back();pending.pop_back();out[j]=i-j;
        }
        pending.push_back(i);
    }
    print_values(out);
''',
496: '''    int n1,n2;cin >> n1 >> n2;auto queries=read_values(n1),a=read_values(n2);
    vector<ll> stack,out;unordered_map<ll,ll> answer;
    for(ll x:a) {while(!stack.empty() && stack.back()<x) {answer[stack.back()]=x;stack.pop_back();}stack.push_back(x);}
    for(ll x:queries) {auto it=answer.find(x);out.push_back(it==answer.end() ? -1 : it->second);}
    print_values(out);
''',
547: '''    int n;cin >> n;vector<vector<int>> g(n,vector<int>(n));for(auto &r:g) for(int &x:r) cin >> x;
    vector<bool> seen(n,false);int components=0;
    for(int i=0;i<n;++i) if(!seen[i]) {
        ++components;vector<int> stack{i};seen[i]=true;
        while(!stack.empty()) {int u=stack.back();stack.pop_back();for(int v=0;v<n;++v)
            if(g[u][v] && !seen[v]) {seen[v]=true;stack.push_back(v);}}
    }
    cout << components << "\\n";
''',
207: '''    int n,e;cin >> n >> e;vector<vector<int>> adj(n);vector<int> indeg(n,0);
    while(e--) {int a,b;cin >> a >> b;adj[b].push_back(a);++indeg[a];}
    queue<int> q;for(int i=0;i<n;++i) if(!indeg[i]) q.push(i);int count=0;
    while(!q.empty()) {int u=q.front();q.pop();++count;for(int v:adj[u]) if(!--indeg[v]) q.push(v);}
    cout << (count==n) << "\\n";
''',
338: '''    int n;cin >> n;vector<int> counts(n+1,0);
    for(int i=1;i<=n;++i) counts[i]=counts[i/2]+i%2;
    print_values(counts);
''',
912: '''    int n;cin >> n;auto a=read_values(n);vector<ll> buffer(n);
    function<void(int,int)> sort_range=[&](int lo,int hi) {
        if(hi-lo<=1) return;int mid=lo+(hi-lo)/2;sort_range(lo,mid);sort_range(mid,hi);
        int i=lo,j=mid,k=lo;
        while(i<mid && j<hi) buffer[k++]=a[i]<=a[j] ? a[i++] : a[j++];
        while(i<mid) buffer[k++]=a[i++];while(j<hi) buffer[k++]=a[j++];
        for(int t=lo;t<hi;++t) a[t]=buffer[t];
    };
    sort_range(0,n);print_values(a);
''',
}


def source(pid):return HEADER+BODIES[pid]+'    return 0;\n}\n'
