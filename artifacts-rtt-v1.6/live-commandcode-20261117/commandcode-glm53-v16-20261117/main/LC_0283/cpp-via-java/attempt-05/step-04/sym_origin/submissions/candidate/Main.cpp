#include <bits/stdc++.h>
using namespace std;
int main(){
    int n;
    if(!(cin>>n)) return 0;
    vector<long long> a(n);
    for(int i=0;i<n;i++) cin>>a[i];
    int w=0;
    for(int r=0;r<n;r++){
        if(a[r]!=0){ swap(a[w],a[r]); w++; }
    }
    for(int i=0;i<n;i++){ if(i) cout<<' '; cout<<a[i]; }
    cout<<'\n';
}