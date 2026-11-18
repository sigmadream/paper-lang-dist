#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if(!(cin >> N)) return 0;

    vector<long long> score(N);
    for(int i = 0; i < N; ++i) cin >> score[i];

    long long ans;
    if(N == 1){
        ans = score[0];
    } else if(N == 2){
        ans = score[0] + score[1];
    } else {
        long long dp0 = 0;
        long long dp1 = score[0];
        long long dp2 = score[0] + score[1];
        long long prev = score[1];

        for(int i = 2; i < N; ++i){
            long long best = max(dp1, dp0 + prev);
            long long dp = best + score[i];

            dp0 = dp1;
            dp1 = dp2;
            dp2 = dp;
            prev = score[i];
        }
        ans = dp2;
    }

    cout << ans << '\n';
    return 0;
}