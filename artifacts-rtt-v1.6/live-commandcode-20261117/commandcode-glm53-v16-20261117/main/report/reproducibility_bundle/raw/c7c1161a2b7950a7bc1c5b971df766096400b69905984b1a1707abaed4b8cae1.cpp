#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n;
    if(!(cin >> n)) return 0;
    vector<long long> a(n);
    for(auto &x : a) cin >> x;
    long long cur = a[0], best = a[0];
    for(size_t i = 1; i < a.size(); ++i){
        cur = max(a[i], cur + a[i]);
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}