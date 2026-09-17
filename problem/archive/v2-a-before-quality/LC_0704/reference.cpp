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
    int n; ll target; cin >> n >> target; auto a=read_values(n);
    int lo=0,hi=n;
    while(lo<hi) {int mid=lo+(hi-lo)/2; if(a[mid]<target) lo=mid+1; else hi=mid;}
    cout << (lo<n && a[lo]==target ? lo : -1) << "\n";
    return 0;
}
