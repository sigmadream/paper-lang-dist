#include <bits/stdc++.h>
using namespace std;
int main(){
    int n, c;
    if(scanf("%d %d", &n, &c)!=2) return 0;
    vector<long long> a(n);
    for(int i=0;i<n;i++) scanf("%lld", &a[i]);
    sort(a.begin(), a.end());
    long long left=1, right=a[n-1]-a[0], ans=0;
    while(left<=right){
        long long mid=(left+right)/2;
        int count=1;
        long long prev=a[0];
        for(int i=1;i<n;i++){
            if(a[i]-prev>=mid){count++;prev=a[i];}
        }
        if(count>=c){ans=mid;left=mid+1;}
        else right=mid-1;
    }
    printf("%lld\n", ans);
    return 0;
}