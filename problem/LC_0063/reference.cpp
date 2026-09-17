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
    int m,n; cin >> m >> n; vector<ll> dp(n,0);dp[0]=1;
    for(int i=0;i<m;++i) for(int j=0;j<n;++j) {
        int blocked;cin >> blocked;
        if(blocked) dp[j]=0;else if(j) dp[j]=min(2000000001LL,dp[j]+dp[j-1]);
    }
    cout << dp.back() << "\n";
    return 0;
}
