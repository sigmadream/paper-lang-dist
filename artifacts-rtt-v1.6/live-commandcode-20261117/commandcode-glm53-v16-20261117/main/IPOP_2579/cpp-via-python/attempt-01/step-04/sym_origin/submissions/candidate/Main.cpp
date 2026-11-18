#include <bits/stdc++.h>
using namespace std;
int main(){
    int n;
    if(!(cin>>n)) return 0;
    vector<long long> score(n+1,0), dp(n+1,0);
    for(int i=1;i<=n;i++) cin>>score[i];
    if(n>=1) dp[1]=score[1];
    if(n>=2) dp[2]=score[1]+score[2];
    for(int i=3;i<=n;i++)
        dp[i]=max(dp[i-2], dp[i-3]+score[i-1])+score[i];
    cout<<dp[n]<<"\n";
}