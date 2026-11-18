#include <bits/stdc++.h>
using namespace std;

int main(){
    int n, c;
    if(scanf("%d %d", &n, &c)!=2) return 0;
    vector<long long> a(n);
    for(int i=0;i<n;i++) scanf("%lld", &a[i]);
    sort(a.begin(), a.end());
    long long lo=1, hi=a[n-1]-a[0], ans=0;
    while(lo<=hi){
        long long mid=lo+(hi-lo)/2;
        long long cnt=1; long long prev=a[0];
        for(int i=1;i<n;i++){
            if(a[i]-prev>=mid){cnt++;prev=a[i];}
        }
        if(cnt>=c){ans=mid;lo=mid+1;}
        else hi=mid-1;
    }
    printf("%lld\n", ans);
    return 0;
}