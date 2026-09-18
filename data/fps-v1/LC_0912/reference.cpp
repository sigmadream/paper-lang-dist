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
    int n;cin >> n;auto a=read_values(n);vector<ll> buffer(n);
    function<void(int,int)> sort_range=[&](int lo,int hi) {
        if(hi-lo<=1) return;int mid=lo+(hi-lo)/2;sort_range(lo,mid);sort_range(mid,hi);
        int i=lo,j=mid,k=lo;
        while(i<mid && j<hi) buffer[k++]=a[i]<=a[j] ? a[i++] : a[j++];
        while(i<mid) buffer[k++]=a[i++];while(j<hi) buffer[k++]=a[j++];
        for(int t=lo;t<hi;++t) a[t]=buffer[t];
    };
    sort_range(0,n);print_values(a);
    return 0;
}
