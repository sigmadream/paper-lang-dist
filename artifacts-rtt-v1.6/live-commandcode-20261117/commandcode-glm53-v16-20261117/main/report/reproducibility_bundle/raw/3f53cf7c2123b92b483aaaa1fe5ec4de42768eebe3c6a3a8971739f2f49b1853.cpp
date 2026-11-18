#include <bits/stdc++.h>
using namespace std;

int main(){
    int n;
    if(!(cin>>n)) return 0;
    vector<int> a(n);
    for(int i=0;i<n;i++) cin>>a[i];
    if(n>0){
        int cur=a[0], best=a[0];
        for(int i=1;i<n;i++){
            cur=max(a[i],cur+a[i]);
            best=max(best,cur);
        }
        cout<<best<<"\n";
    }
    return 0;
}