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
    string s; int k; cin >> s >> k; vector<string> words(k); for(auto &w:words) cin >> w;
    vector<bool> dp(s.size()+1,false);dp[0]=true;
    for(size_t i=1;i<=s.size();++i) for(const auto &w:words)
        if(w.size()<=i && dp[i-w.size()] && s.compare(i-w.size(),w.size(),w)==0) {dp[i]=true;break;}
    cout << dp.back() << "\n";
    return 0;
}
