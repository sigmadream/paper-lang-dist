#include <cstdio>
#include <vector>

int main() {
    int M, N;
    if (std::scanf("%d %d", &M, &N) != 2) return 0;

    std::vector<long long> dp(N, 1);
    for (int i = 1; i < M; ++i) {
        for (int j = 1; j < N; ++j) {
            dp[j] += dp[j - 1];
        }
    }

    std::printf("%lld\n", dp[N - 1]);
    return 0;
}