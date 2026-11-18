#include <bits/stdc++.h>
using namespace std;

int main(){
    long long n;
    if(!(cin>>n)) return 0;
    vector<long long> a(n);
    for(auto &x:a) cin>>x;
    size_t w=0;
    for(size_t r=0;r<a.size();++r){
        if(a[r]!=0){ swap(a[w],a[r]); ++w; }
    }
    for(size_t i=0;i<a.size();++i){
        if(i) cout<<' ';
        cout<<a[i];
    }
    cout<<'\n';
    return 0;
}