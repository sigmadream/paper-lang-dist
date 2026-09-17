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
    string s,t; cin >> s >> t; array<int,26> counts{};
    for(char c:s) ++counts[c-'a']; for(char c:t) --counts[c-'a'];
    cout << all_of(counts.begin(),counts.end(),[](int x){return x==0;}) << "\n";
    return 0;
}
