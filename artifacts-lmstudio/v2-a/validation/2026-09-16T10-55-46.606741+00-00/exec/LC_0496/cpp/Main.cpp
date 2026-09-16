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
    int n1,n2;cin >> n1 >> n2;auto queries=read_values(n1),a=read_values(n2);
    vector<ll> stack,out;unordered_map<ll,ll> answer;
    for(ll x:a) {while(!stack.empty() && stack.back()<x) {answer[stack.back()]=x;stack.pop_back();}stack.push_back(x);}
    for(ll x:queries) {auto it=answer.find(x);out.push_back(it==answer.end() ? -1 : it->second);}
    print_values(out);
    return 0;
}
