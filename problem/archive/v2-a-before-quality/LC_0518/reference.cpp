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
    int amount,k; cin >> amount >> k; auto coins=read_values(k);
    vector<unsigned long long> dp(amount+1,0);dp[0]=1;
    for(ll coin:coins) for(int x=(int)coin;x<=amount;++x)
        dp[x]=min(2147483648ULL,dp[x]+dp[x-coin]);
    cout << dp[amount] << "\n";
    return 0;
}
