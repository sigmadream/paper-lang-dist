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
    string s; getline(cin,s); if(!s.empty() && s.back()=='\r') s.pop_back();
    array<int,256> last; last.fill(-1); int start=0,best=0;
    for(int i=0;i<(int)s.size();++i) {
        unsigned char c=s[i]; start=max(start,last[c]+1);best=max(best,i-start+1);last[c]=i;
    }
    cout << best << "\n";
    return 0;
}
