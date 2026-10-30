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
    int n; cin >> n;auto a=read_values(n);vector<int> out(n,0),pending;
    for(int i=0;i<n;++i) {
        while(!pending.empty() && a[pending.back()]<a[i]) {
            int j=pending.back();pending.pop_back();out[j]=i-j;
        }
        pending.push_back(i);
    }
    print_values(out);
    return 0;
}
