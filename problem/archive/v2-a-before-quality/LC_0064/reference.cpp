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
    int m,n; cin >> m >> n; vector<ll> dp(n,LLONG_MAX/4);
    for(int i=0;i<m;++i) for(int j=0;j<n;++j) {
        ll value;cin >> value;
        if(!i && !j) dp[j]=value;
        else dp[j]=value+min(dp[j],j ? dp[j-1] : LLONG_MAX/4);
    }
    cout << dp.back() << "\n";
    return 0;
}
