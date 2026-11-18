#include <bits/stdc++.h>
using namespace std;

int main(){
    int n; long long c;
    if(scanf("%d %lld", &n, &c)!=2) return 0;
    vector<long long> s(n);
    for(int i=0;i<n;i++) scanf("%lld",&s[i]);
    sort(s.begin(), s.end());
    long long lo=1, hi=s[n-1]-s[0], ans=0;
    while(lo<=hi){
        long long mid=lo+(hi-lo)/2;
        long long k=1, p=s[0];
        for(int i=1;i<n;i++){
            if(s[i]-p>=mid){ k++; p=s[i]; }
        }
        if(k>=c){ ans=mid; lo=mid+1; } else hi=mid-1;
    }
    printf("%lld\n", ans);
    return 0;
}