#include <bits/stdc++.h>
using namespace std;

int main(){
    int n;
    if(!(cin>>n)) return 0;
    vector<int> a(n);
    for(auto &x: a) cin>>x;
    long long best=a[0], cur=a[0];
    for(int i=1;i<n;i++){
        cur = max((long long)a[i], cur+a[i]);
        best = max(best, cur);
    }
    cout<<best<<"\n";
    return 0;
}