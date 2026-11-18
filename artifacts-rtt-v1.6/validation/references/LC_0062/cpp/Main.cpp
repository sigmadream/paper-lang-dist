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
    int m,n; cin >> m >> n; vector<ll> dp(n,1);
    for(int i=1;i<m;++i) for(int j=1;j<n;++j) dp[j]+=dp[j-1];
    cout << dp.back() << "\n";
    return 0;
}
